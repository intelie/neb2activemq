# -*- coding: utf-8 -*-

import sys
import types
import sys
import time
import logging
import Queue
import inspect
import threading
import time
import socket
import copy
import json
from utils import neb_parser
import stomp #stomp have an utils.py! Import AFTER neb_parser

#TODO Move this to settings or to an environment option 
PROFILE_MEM = False

logger = logging.getLogger("nebpublisher.manager")
memlogger = logging.getLogger("nebpublisher.memprofiler")

#For testing, replace 2 lines above to:
#logger = logging.getLogger('stomp-logger')
#handler = logging.Handler()
#def print_message(x):
#    print x
#handler.emit = print_message
#logger.addHandler(handler)

#used only to profile Memory usage
if PROFILE_MEM :
    try:  
        import guppy.heapy.heapyc
        from guppy import hpy
    except ImportError:
        logger.error("Couldn't import Guppy module.")
        PROFILE_MEM = False

    # time in seconds for memory reports to be logged
    interval = 60

try:
    import sysv_ipc
except ImportError: 
    logger.error("Couldn't import sysv_ipc module. It must me installed from http://semanchuk.com/philip/sysv_ipc/")
    exit(1)

class Manager(object):
    """ Responsible for initializing components:
         - OS message queue subscriber and parses (Subscriber)
         - Actimq sender via stomp (QueueProcessor)
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
          Check if Nagios is using the same key and is running " % settings.OS_MQ_KEY )
          exit(1)
            
        #start execution      
        self.parser = neb_parser.Parser(self.topics, self.parser_functions)  
        self.subscriber = Subscriber("subscriber", self.mq, settings, self.parser, self.queue).start();                   
          
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
    if PROFILE_MEM:
      memlogger.debug("Initiating memory profiler for subscriber")
      self.hp = hpy()
    
  def run (self):
    if PROFILE_MEM :
      time_ref = time.time()
      self.hp.setrelheap()
    
    while True:
      try:
        logger.debug("Waiting for a OS message:")
        
        #This reception blocks until some new message appears. Other option is to use flag IPC_NOWAIT
        message, message_type = self.mq.receive()
        message = str(message)
				
        if (message.find('\0') < 0):
          logger.warn("Message should end with '\\0' character")
          pass
        
        message, char, garbage = message.partition('\0')
        
        logger.debug("Message received. Type: %i Message: %s" %(message_type, str(message)))

        events = self.parser.parse(message_type, str(message))

        if events != neb_parser.NOT_IMPLEMENTED and events != neb_parser.BAD_FORMAT:
          for event in events:
            if event != neb_parser.NOT_IMPLEMENTED and event != neb_parser.BAD_FORMAT:
              self.publish(event)

        if PROFILE_MEM:
          if time.time() > time_ref + interval:
            memlogger.debug(self.hp.heap())
            time_ref = time.time()
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
    if (self.queue.full()):
      self.queue.get_nowait()
      logger.warn("Queue between process is full. Dropping old messages")
    if (not self.queue.full()):
      self.queue.put((header, body))
      logger.debug("Message on queue")
    

class QueueProcessor(object):
    """ Responsible for processing objects in queue """
    def __init__(self, queue, settings):
        self.queue = queue
        self.connection = ConnectionAdapter(settings.BROKER, settings.CONN_SLEEP_DELAY) 
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
                    logger.debug("New message taken from queue %s %s" % (str(header), str(body) ) )
                 
                try:
                    msg = json.dumps(body)
                except UnicodeDecodeError:
                    try:
                        enc = chardet.detect(body)['encoding']
                        msg = json.dumps(body, encoding=enc)
                    except:
                        logger.error("UnicodeDecodeError on Queuprocessor.process - can't use chardet, discarding message")
                        msg = None
                finally:
                    if msg is not None:
                        self.connection.send(msg, header, destination=header['destination'])
                    sent = True
                
            except Queue.Empty:
              logger.debug(" --Empty queue-- ")
              continue
            
            except KeyboardInterrupt:
              logger.info("User interrupted. Shutting down.")
              exit(0)
              
            except socket.error:
              #try to reconnect
              logger.error("Socket error >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
              self.connection = ConnectionAdapter(self.settings.BROKER, self.settings.CONN_SLEEP_DELAY)
            
            except Exception, e:
              logger.error('Unknown exception %s' % str(sys.exc_info()))
              #TODO: Maybe retry
              continue


class ConnectionAdapter(object):
  """Integrates with a the STOMP client API.
  ConnectionAdapter is an easy-to-use way to send messages via stomp
  """
  def __init__(self, broker, conn_sleep_delay):
    self.broker = broker
    self.conn_sleep_delay = conn_sleep_delay
    self.__connect()


  def send(self, message, headers={}, **keyword_headers):
    try:
      self.conn.send(message, headers, **keyword_headers)
    except stomp.internal.exception.NotConnectedException:
      logger.error("Lost connection with %s. Trying to reconnect." % \
                   self.broker)
      time.sleep(self.conn_sleep_delay)
      self.__connect()
      self.send(message, headers, **keyword_headers)
  

  def __connect(self):
    """Attempts to connect to broker(s).
    stomp will automatically try to connect to other brokers
    if some of them are offline.
    """
    connection = stomp.Connection(self.broker, prefer_localhost=False,
                                  try_loopback_connect=False)
    connection.set_listener('', ErrorListener(connection))
    connection.start()
    connection.connect()
    self.conn = connection

    #What do we need it for?
    #except Exception:
    #  if type(sys.exc_info()[1]) == types.TupleType:
    #    exc = sys.exc_info()[1][1]
    #  else:
    #    exc = sys.exc_info()[1]
    #    logger.error('Unexpected error %s.' % (exc))
    #    return connection
    #else:
    #  return connection


class ErrorListener(stomp.ConnectionListener):
  def __init__(self, connection):
    self.connection = connection
    
  def on_error(self, headers, message):
    logger.error('received an error %s' % message)
    if self.connection.is_connected:
      # This necessary because of an activemq bug - https://issues.apache.org/activemq/browse/AMQ-1376
      logger.error('TCP is connect but has some errors')
      self.connection.stop()



if __name__ == '__main__':
  print 'Testing...'
  brokers = [('192.168.0.44', 61613), ('192.168.0.77', 61613)]
  conn = ConnectionAdapter(brokers, 0)
  while True:
      try:
          string_to_send = 'testing ' + str(time.time())
          to_send = {'message': string_to_send,
                     'headers': {'destination': '/queue/events'}}
          print 'sent: %s' % string_to_send
          conn.send(**to_send)
          time.sleep(1)
      except KeyboardInterrupt:
          break
  sys.exit()
  #conn.conn.disconnect()
