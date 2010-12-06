#!/usr/bin/env python
# coding: utf-8

import stomp
import json
import sys
import time

if len(sys.argv) < 3:
    print 'Usage: %s <server-hostname> <#-online-users>' % sys.argv[0]
    sys.exit(1)

broker = [('localhost', 61613)]
amq = stomp.Connection(broker)
amq.start()
amq.connect()
msg = {'host': sys.argv[1], 'online_users': sys.argv[2], 'state': 'OK'}
headers = {'destination': '/queue/events', 'timestamp': long(time.time()) * 1000, 'eventtype': 'VideoServerUsers'}
amq.send(json.dumps(msg), headers)
