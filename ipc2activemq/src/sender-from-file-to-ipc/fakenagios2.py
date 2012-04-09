import sysv_ipc
import re
import time
import datetime


def send_message(mq, message):
    print 'Trying to send: ', message
    try:
        mq.send(message, block=False, type=13)
    except sysv_ipc.BusyError:
        print "Queue is full, ignoring"

def send_messages(mq, service_counter, status_counter, test_service, downtime=1,
                  host='some_host'):
    try:
        for key, item in test_service.iteritems():
            if type(item) == str:
                #message = '%s^%s^%s^%s^0\0' % (host, key, status_counter, item)
                message = '%s^%s^%s^%i^%s\0' % (host, key, status_counter,
                        downtime, item)
                send_message(mq, message)
            elif type(item) == list:
                for msg in item:
                    #message = '%s^%s^%s^%s^0\0' % (host, key, status_counter, msg)
                    message = '%s^%s^%s^%i^%s\0' % (host, key, status_counter,
                            downtime, msg)
                    send_message(mq, message)
    except Exception as e:
        print "Caugh an unknown exception, ignoring.", e
        pass


def main(test_service):
    mq = sysv_ipc.MessageQueue(123456, flags=sysv_ipc.IPC_CREAT, mode=0666)
    msg_counter = 0
    service_counter = status_counter = 0
    init_time = time.time()
    msg_init_time = time.time()
    if True:
        try:
            now = datetime.datetime.fromtimestamp(time.time())
            messages_on_queue = mq.current_messages
                # Send message
            send_messages(mq, service_counter, status_counter, test_service)
            status_counter = (status_counter + 1) % 4
            if status_counter == 0:
                service_counter = (service_counter + 1) % 8
                # Calc time to sleep
            msg_counter = msg_counter + 1
            now = time.time()
        except KeyboardInterrupt:
            print "User interrupted. Shutting down."
            exit(0)
        except sysv_ipc.ExistentialError:
            print "Message queue does not exist for key"
            exit(1)
