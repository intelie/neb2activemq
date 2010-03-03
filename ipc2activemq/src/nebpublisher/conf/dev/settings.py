# -*- coding: utf-8 -*-
import os, socket, sys
from nebpublisher import logger, utils


#### Main settings ####

BROKER=[('localhost', 61613)]     # Message Broker Target
CONN_SLEEP_DELAY = 3            # Time to way after a connection was lost

MAX_QUEUE_SIZE = 100            # Max queue size. If equals to 0, queue is unbound!
QUEUE_SLEEP_TIME = 3            # Tempo que a thread espera se a queue estiver vazia



OS_MQ_SLEEP = 1                 # tempo que espera antes de ler novamente
OS_MQ_KEY=123456                # id to be used on OS message queue creation

#Local configuration for testing purposes
EVENT_TYPE = 'eventtype'
DESTINATION = { 'destination' : '/queue/events' } # will be inherited for each config

