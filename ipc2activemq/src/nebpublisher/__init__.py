import logging, logging.config, os

__all__ = ["manager", "utils"]


#defines global logger
log_conf = [os.path.join( os.path.dirname(__file__), "conf/log.ini"), "conf/log.ini"][os.path.isfile("log.ini")]
 
if( os.path.isfile(log_conf) ):
    print "configuring log from log.ini"
    logging.config.fileConfig(log_conf)
else:
    print "no log.ini was found"
    logging.basicConfig()
        
logger = logging.getLogger("root")



