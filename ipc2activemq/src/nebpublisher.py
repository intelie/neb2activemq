# -*- coding: utf-8 -*-

""" Run neb publisher """

import os, sys, getopt, optparse, imp
from nebpublisher import manager
from nebpublisher.utils.misc import run_as_daemon

import cProfile

PIDFILE=os.path.join( os.path.abspath(os.path.dirname(__file__)), '/usr/local/nagios/var/nebpublisher.pid')
DAEMON=True
PROFILE=False
ENV="dev"

def main():
    #read settings module
    conf_dir = os.path.join( os.path.abspath(os.path.dirname(__file__)), "nebpublisher/conf/" + ENV )
    settings_path = os.path.join(conf_dir, "settings.py")
    topics_path = os.path.join(conf_dir, "topics.py")

    #read settings
    fin = open(settings_path, 'rb')
    settings = imp.load_source("settings", settings_path, fin)
  

    #read topics
    fin = open(topics_path, 'rb')
    topics = imp.load_source("topics", topics_path, fin)

    #run manager with defined settings
    def main_fn(): manager.Manager(settings, topics)
    if DAEMON:
        run_as_daemon(main_fn, PIDFILE)
    else:
        main_fn()  


if __name__ == "__main__":
    
    parser = optparse.OptionParser()
    parser.add_option('--nodaemon',
                      dest="nodaemon",
                      default=not DAEMON,
                      action="store_true",
                      )
    parser.add_option('-p','--pidfile',
                      dest="pidfile",
                      default=PIDFILE,
                      type="string",
                      )
    parser.add_option('--profile',
                      dest="profile",
                      default=PROFILE,
                      action="store_true",
                      )
    parser.add_option('--env',
                      dest="env",
                      default=ENV,
                      type="string"
                      )
    options, remainder = parser.parse_args()
   

    DAEMON = not options.nodaemon
    PIDFILE = options.pidfile
    PROFILE = options.profile
    ENV = options.env

    print "Running nebpublisher."
    print "Environment: %s" % ENV
    print "Running as daemon: %s" % DAEMON
    print "Pidfile: %s" % PIDFILE  
    print "Running with profiler: %s" % PROFILE
  
    if PROFILE:
        cProfile.run('main()', 'profile.log')
    else:
        main()
