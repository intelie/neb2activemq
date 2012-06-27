# -*- coding: utf-8 -*-
import os
import socket
import sys
from nebpublisher import logger, utils


#Main settings
BROKER = [('localhost', 61613)] # Message Broker Target
CONN_SLEEP_DELAY = 3 # Time to way after a connection was lost
MAX_QUEUE_SIZE = 100 # Max queue size. If equals to 0, queue is unbound!
QUEUE_SLEEP_TIME = 3 # Time to wait if queue is empty
OS_MQ_SLEEP = 1 # Time to wait before reading again
OS_MQ_KEY=123456 # id to be used on OS message queue creation
OS_MQ_MAX_MSG_SIZE=35000 #Max IPC Queue message size in bytes


#Local configuration for testing purposes
EVENT_TYPE = 'eventtype'
DESTINATION = {'destination': '/queue/events'} # will be inherited for each config

FILTER_HOSTS = False
ALLOWED_HOSTS = tuple()

#Location of the processed checks types file
PROC_CHECK_TYPES_FILE = '/var/log/nagios/usedChecks.txt'

#Location of the file that contains the name of the checks that are not yet 
#registered on topics.py
NOT_REGISTERED_CHECKS_FILE = '/var/log/nagios/notRegisteredChecks.txt'

#Location of the file containing the log entries that did not match an existing 
#regexp for its event type
NO_MATCH_MSGS_FILE = '/var/log/nagios/noMatchMsgs.txt'
NO_MATCH_MSGS_MAX_FILE_SIZE_IN_BYTES = 102400


