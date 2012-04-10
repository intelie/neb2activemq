#!/bin/sh

ENV=prod

DAEMON=ipc2activemq.py
NAME=nebpublisher
DESC="nebpublisher daemon"

if [ -z "$PIDFILE" ] ; then	
	if(test -f "$NAME.pid") then
		PIDFILE=$NAME.pid
	else
		PIDFILE=/var/run/nagios/$NAME.pid	
	fi
fi

startdaemon(){

    # need do test if the file is owned by nagios user or It will return an error
    if [ -f $PIDFILE ]; then
        OWNER=`ls -l $PIDFILE | tr " " ":" | cut -d":" -f3`
        if [ $OWNER != "nagios" ]; then
            echo "\n$PIDFILE isn't owned by nagios user\n"         
            return
        fi 
    fi
    if(test -f $PIDFILE && ps -p `cat $PIDFILE` > /dev/null); then
        echo "Daemon is running: $PIDFILE \n" 
    else
        echo "Starting $DESC: $DAEMON \n"
        sudo -u nagios python2.6 $DAEMON --pidfile=$PIDFILE --env=$ENV
    fi
}

stopdaemon(){
  echo -n "Stoping $DESC: \n"
  if(test -f $PIDFILE) then
    pid=`head -1 $PIDFILE`  
    echo "\t stoping $pid \n"
    sudo -u nagios kill $pid
    sudo -u nagios rm $PIDFILE
  else
    echo "Pid file not found: $PIDFILE \n"
    echo "Try force-stop to kill all process \n"
  fi
}

forcestop(){
  sudo -u nagios ps -ef | grep  ipc2activemq.py | grep -v grep | awk '{ print $2 }'| xargs kill -9
}

test -f $DAEMON || exit 0

set -e

case "$1" in
  start)
    startdaemon
  ;;
  stop)
    stopdaemon 
  ;;
  restart)
  echo -n "Restarting $DESC: "
    stopdaemon
    startdaemon
  ;;
  force-stop)
    echo -n "Force stopping $DESC \n"
    forcestop
    if(test -f $PIDFILE) then
      rm $PIDFILE
    fi
  ;;
  *)
  N=/etc/init.d/$NAME
  echo "Usage: $N {start|stop|restart|force-stop}" >&2
  exit 1
  ;;
esac

exit 0
