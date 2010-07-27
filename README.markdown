neb2activemq
============

This project is composed of two separated systems.

The first uses Nagios Event Broker to collect service checks data and send this info through IPC using a UNIX message queue. This was written in C.

The second reads from a message queue, parse the messages to a JSON event, and, via STOMP protocol, sends to Activemq queue. This was written in Python.

Available under GNU General Public License v3.


Dependencies
============

This software depends on:

- Python 2.6: http://www.python.org/download/

- sysv_ipc: http://pypi.python.org/pypi/sysv_ipc
  Just execute: # easy_install sysv_ipc

- stomppy: http://stomppy.googlecode.com/
  Download, unpack and execute: # python2.6 setup.py install

- chardet: http://chardet.feedparser.org/
  Download, unpack and execute: # python2.6 setup.py install
