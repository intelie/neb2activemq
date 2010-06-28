import time
import sys

import stomp

class MyListener(object):
    def on_error(self, headers, message):
        print 'received an error %s' % message

    def on_message(self, headers, message):
        print 'received a message %s' % message

brokers = [('192.168.0.44', 61613), ('192.168.0.77', 61613)]
conn = stomp.Connection(brokers, prefer_localhost=False,
                        try_loopback_connect=False)
conn.set_listener('', MyListener())
conn.start()
conn.connect()

conn.subscribe(destination='/queue/events', ack='auto')
#conn.send(' '.join(sys.argv[1:]), destination='/queue/test')

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        sys.exit()
conn.disconnect()
