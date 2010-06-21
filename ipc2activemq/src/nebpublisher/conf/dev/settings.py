# -*- coding: utf-8 -*-
import os
import socket
import sys
from nebpublisher import logger, utils


#Main settings
BROKER = [('192.168.42.105', 61613)] # Message Broker Target
CONN_SLEEP_DELAY = 3 # Time to way after a connection was lost
MAX_QUEUE_SIZE = 100 # Max queue size. If equals to 0, queue is unbound!
QUEUE_SLEEP_TIME = 3 # Time to wait if queue is empty
OS_MQ_SLEEP = 1 # Time to wait before reading again
OS_MQ_KEY=123456 # id to be used on OS message queue creation


#Local configuration for testing purposes
EVENT_TYPE = 'eventtype'
DESTINATION = {'destination': '/queue/events'} # will be inherited for each config
