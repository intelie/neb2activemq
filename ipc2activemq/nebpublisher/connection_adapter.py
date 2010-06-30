import stomp
import logging
import time
import sys


logger = logging.getLogger("nebpublisher.manager")


class ConnectionAdapter(object):
    """
      Adapter to send messages to activemq through STOMP.       
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
    brokers = [('127.0.0.1', 61613), ('127.0.0.1', 61613)]
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
