"""Util functions"""

from __future__ import with_statement
import threading
import signal
import inspect
import math, random
import Queue
import time, logging, sys
import os

#allow logging per module
logger = logging.getLogger("watson.utils") 


def run_as_daemon(fn, pidfile):
    logger.info("Running as deamon")
    # do the UNIX double-fork
    # Decouple from user session terminal process
    try:
        pid = os.fork()
        if pid:
            sys.exit(0) # exit first parent
    except OSError, e:
        logger.error("fork #1 failed: %d (%s)" % (e.errno, e.strerror))
        sys.exit(1)

    # decouple from parent environment
    os.chdir("/") #don't prevent unmounting...
    os.setsid()
    os.umask(0)

    # do second fork
    try:
        pid = os.fork()
        if pid and pidfile:
            pidfile_fp = open(pidfile, 'w')
            pidfile_fp.write("%d" % pid)
            pidfile_fp.close()
            sys.exit(0)
    except OSError, e:
        logger.error("fork #2 failed: %d (%s)" % (e.errno, e.strerror))
        sys.exit(1)
    fn()


def daemonize(really_run_as_deamon, pidfile=None):
    """Generator for creating a forked process
    from a function"""

    signal_subscribe()
    #Allows a parameter to configure
    if really_run_as_deamon:
        def fn():
            pass
        run_as_daemon(fn)

    def wrap(f):
        def wrapped_f(*args, **kwargs):
            """Wrapper function to be returned from generator.
            Executes the function bound to the generator and then
            exits the process"""
            f(*args, **kwargs)
        return wrapped_f
    return wrap


def signal_subscribe():
    """Handle system signals"""  
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

# signal_handler function only deals with process termination 
def signal_handler(signum, frame):
    """Handle system signals"""
    logger.info('Closing the program!')
    exit()
