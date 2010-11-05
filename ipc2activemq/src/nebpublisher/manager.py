# coding: utf-8

import sys
import types
import time
import logging
import Queue
import inspect
import threading
import socket
import copy
import json
from utils import neb_parser
from connection_adapter import *
import threading
import glob
import os
import socket


logger = logging.getLogger("nebpublisher.manager")
hostname = socket.gethostname()

try:
    import chardet
except ImportError:
    logger.error('chardet is not installed - manager will discard all messages \
if UnicodeDecodeError is raised')


class FileMonitor(threading.Thread):
    def __init__(self, filename, wildcard, stat_check_time=1):
        threading.Thread.__init__(self)
        self.wildcard = wildcard
        self.filename = filename
        self.stat_check_time = stat_check_time

        self.should_run = threading.Event()
        self.new_file = threading.Event()
        self.should_run.set()
        self.new_file.clear()

        try:
            self.stat_filename = os.stat(filename)
        except OSError:
            self.stat_filename = -1


    def run(self):
        while self.should_run.is_set():
            last_modified = FileMonitor.get_last_modified(self.wildcard)
            if not last_modified:
                time.sleep(self.stat_check_time)
                continue
            try:
                stat_last_modified = os.stat(last_modified)
            except OSError:
                time.sleep(self.stat_check_time)
                continue
            if last_modified != self.filename and \
               stat_last_modified[-2] >= self.stat_filename[-2] or \
               last_modified == self.filename and \
               stat_last_modified[-3] > self.stat_filename[-3]:
                self.filename = last_modified
                self.stat_filename = os.stat(last_modified)
                self.new_file.set()

            time.sleep(self.stat_check_time)


    @staticmethod
    def get_last_modified(wildcard):
        filenames = {}
        for filename in glob.glob(wildcard):
            try:
                stat = os.stat(filename)
            except:
                continue
            filenames[stat[-2]] = filename
        if len(filenames):
            timestamps = filenames.keys()
            timestamps.sort()
            last_modified = filenames[timestamps[-1]]
            return last_modified
        return None


class Subscriber(threading.Thread):
    def __init__(self, filename, go_to_the_end, settings, parser, queue,
                 seek_time=0.1):
        threading.Thread.__init__(self)
        self.settings = settings
        self.parser = parser
        self.queue = queue
        self.header = settings.DESTINATION

        self.should_run = threading.Event()
        self.should_run.set()

        self.seek_time = seek_time
        self.filename = filename
        self.fp = open(filename, 'r')
        if go_to_the_end:
            self.fp.seek(0, 2)


    def run(self):
        message_type = self.settings.LOG_MESSAGE_TYPE
        while self.should_run.is_set():
            new_line = self.fp.readline()
            if new_line:
                message = '%s^%s^%s^%s' % (hostname, 'check_log', '0', new_line)
                events = self.parser.parse(message_type, message)
                if events != neb_parser.NOT_IMPLEMENTED and events != neb_parser.BAD_FORMAT:
                    for event in events:
                        if event != neb_parser.NOT_IMPLEMENTED and event != neb_parser.BAD_FORMAT:
                            self.publish(event)
            else:
                time.sleep(self.seek_time)


    def publish(self, event):
        self.header.update({'timestamp': long(time.time()) * 1000})
        self.header.update({'eventtype': event['eventtype']})
        del event['eventtype']

        # Do not use references to avoid queue mismatches
        header = copy.copy(self.header)
        body = copy.copy(event)
        logger.debug("EVENT ---  %s %s" % (str(body), str(header)))
        if self.queue.full():
            self.queue.get_nowait()
            logger.warn("Queue between process is full. Dropping old messages")
        if not self.queue.full():
            self.queue.put((header, body))
            logger.debug("Message on queue")


class Manager(object):
    def __init__(self, settings, topics, parser_functions):
        logger.debug("Initiating General Log Manager")
        self.settings = settings
        self.topics = topics
        self.parser_functions = parser_functions

        self.parser = neb_parser.Parser(self.topics, self.parser_functions)
        log_managers = []
        for logfile in self.settings.LOG_FILES:
            print 'iniciando LogManager para %s' % logfile
            log_manager = LogManager(settings, topics, parser_functions,
                                     logfile)
            log_managers.append(log_manager)
            log_manager.start()

        try:
            time.sleep(1)
        except KeyboardInterrupt:
            for log_manager in log_managers:
                log_manager.should_run.clear()
            sys.exit()


class LogManager(threading.Thread):


    def __init__(self, settings, topics, parser_functions, wildcard,
                 check_new_file_time=0.1):
        threading.Thread.__init__(self)
        logger.debug("Initiating LogManager for %s" % wildcard)
        self.topics = topics
        self.parser_functions = parser_functions
        self.settings = settings
        self.check_new_file_time = check_new_file_time

        self.should_run = threading.Event()
        self.should_run.set()
        go_to_the_end = True
        filename = FileMonitor.get_last_modified(wildcard)
        if not filename:
            go_to_the_end = False
            while not filename:
                try:
                    filename = FileMonitor.get_last_modified(wildcard)
                    time.sleep(check_new_file_time)
                except KeyboardInterrupt:
                    sys.exit(0)

        self.parser = neb_parser.Parser(self.topics, self.parser_functions)
        self.queue = Queue.Queue(settings.MAX_QUEUE_SIZE)
        self.subscriber = Subscriber(filename, go_to_the_end, settings,
                                     self.parser, self.queue)
        self.file_monitor = FileMonitor(filename, wildcard)
        self.processor = QueueProcessor(self.queue, settings)
        self.subscriber.start()
        self.file_monitor.start()
        self.processor.start()
       

    def run(self):
        while self.should_run.is_set():
            if self.file_monitor.new_file.is_set():
                self.subscriber.should_run.clear()
                del self.subscriber
                self.subscriber = Subscriber(self.file_monitor.filename,
                                             False,
                                             self.settings,
                                             self.parser, self.queue)
                self.subscriber.start()
                self.file_monitor.new_file.clear()

            time.sleep(self.check_new_file_time)

        self.file_monitor.should_run.clear()
        self.subscriber.should_run.clear()



class QueueProcessor(threading.Thread):
    """ Responsible for processing objects in queue """
    def __init__(self, queue, settings):
        threading.Thread.__init__(self)
        self.queue = queue
        self.connection = ConnectionAdapter(settings.BROKER,
                                            settings.CONN_SLEEP_DELAY)
        self.settings = settings


    def run(self):
        max_messages = -1
        sent = True
        processed_messages = 0
        while processed_messages != max_messages:
            try:
                if sent:
                    #block if queue is empty
                    header, body = self.queue.get(True)
                    processed_messages += 1
                    logger.debug("HEADER %s" % str(header))
                    logger.debug("BODY %s" % str(body))
                    sent = False
                    logger.debug("New message taken from queue %s %s" % \
                                 (str(header), str(body)))
                    if 'host' in body and 'FILTER_HOSTS' in dir(self.settings) \
                       and self.settings.FILTER_HOSTS \
                       and body['host'] not in self.settings.ALLOWED_HOSTS:
                        logger.debug('Host filter is enabled and host "%s" is not in the list - discarding event!' % \
                                     body['host'])
                        continue
                try:
                    msg = json.dumps(body)
                except UnicodeDecodeError:
                    try:
                        enc = chardet.detect(body)['encoding']
                        msg = json.dumps(body, encoding=enc)
                    except Exception:
                        try:
                            err = str(body)
                        except:
                            err = "*can't convert message to string*"
                        logger.error("UnicodeDecodeError on Queuprocessor.process. \
Discarding message. Exception: %s; Message: %s" %  (str(sys.exc_info()), err))
                        msg = None
                finally:
                    if msg is not None:
                        self.connection.send(msg, header,
                                             destination=header['destination'])
                    sent = True
            except Queue.Empty:
                logger.debug(" --Empty queue-- ")
                continue
            except KeyboardInterrupt:
                logger.info("User interrupted. Shutting down.")
                exit(0)
            except socket.error:
                #try to reconnect
                logger.error("Socket error!")
                self.connection = ConnectionAdapter(self.settings.BROKER,
                        self.settings.CONN_SLEEP_DELAY)
            except Exception, e:
                logger.error('Unknown exception %s' % str(sys.exc_info()))
                #TODO: Maybe retry
                continue
