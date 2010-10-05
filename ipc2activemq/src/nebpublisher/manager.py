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


logger = logging.getLogger("nebpublisher.manager")


try:
    import chardet
except ImportError:
    logger.error('chardet is not installed - manager will discard all messages \
if UnicodeDecodeError is raised')


try:
    import sysv_ipc
except ImportError:
    logger.error("Could not import sysv_ipc. See README for installation instructions.")
    exit(1)


class Manager(object):
    """ Responsible for initializing components:
         - OS message queue subscriber and parses (Subscriber)
         - ActiveMQ sender via stomp (QueueProcessor)
    """
    def __init__(self, settings, topics, parser_functions):
        logger.debug("Initiating Manager")
        self.settings = settings
        self.topics = topics
        self.parser_functions = parser_functions

        #queue to send results to broker
        self.queue = Queue.Queue(settings.MAX_QUEUE_SIZE)
        try:
            self.mq = sysv_ipc.MessageQueue(settings.OS_MQ_KEY)
        except sysv_ipc.ExistentialError:
            logger.error("Message queue does not exist for key %i . \
            Check if Nagios is using the same key and is running " % settings.OS_MQ_KEY)
            exit(1)

        #start execution
        self.parser = neb_parser.Parser(self.topics, self.parser_functions)
        self.subscriber = Subscriber("subscriber", self.mq, settings,
                                     self.parser, self.queue)
        self.subscriber.start()
        self.processor = QueueProcessor(self.queue, self.settings)

        #main thread will be processing
        self.processor.process()


class Subscriber(threading.Thread):
    def __init__ (self, name, mq, settings, parser, queue):
        threading.Thread.__init__(self)
        self.name = name
        self.mq = mq
        self.settings = settings
        self.parser = parser
        self.queue = queue
        self.header = settings.DESTINATION

    def run (self):
        while True:
            try:
                logger.debug("Waiting for a OS message:")

                #This reception blocks until some new message appears. Other option is to use flag IPC_NOWAIT
                message, message_type = self.mq.receive()
                message = str(message)
                if message.find('\0') < 0:
                    logger.warn("Message should end with '\\0' character")
                    pass
                message, char, garbage = message.partition('\0')
                logger.debug("Message received. Type: %i Message: %s" %(message_type, str(message)))
                events = self.parser.parse(message_type, str(message))
                if events != neb_parser.NOT_IMPLEMENTED and events != neb_parser.BAD_FORMAT:
                    for event in events:
                        if event != neb_parser.NOT_IMPLEMENTED and event != neb_parser.BAD_FORMAT:
                            self.publish(event)

            except sysv_ipc.PermissionsError, sysv_ipc.ExistentialError:
                logger.error("Message could not be received. Check if os queue exist and its permission")
                time.sleep(self.settings.OS_MQ_SLEEP)
                pass
            except sysv_ipc.InternalError:
                logger.error("A severe error ocurred in os message queue. Aborting..")
                exit(1)
            except Exception, e:
                logger.error('Unknown exception %s' % str(sys.exc_info()))
                exit(1)


    def publish(self, event):
        """ Commmon logic for publish event into queue """
        self.header.update({'timestamp': long(time.time())*1000})
        self.header.update({'eventtype': event['eventtype'] })
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


class QueueProcessor(object):
    """ Responsible for processing objects in queue """
    def __init__(self, queue, settings):
        self.queue = queue
        self.connection = ConnectionAdapter(settings.BROKER,
                                            settings.CONN_SLEEP_DELAY)
        self.settings = settings


    def process(self, max_messages=-1):
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
