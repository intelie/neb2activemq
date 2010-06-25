import sys
import sysv_ipc
import re
import time
import datetime


def send_message(message):
    print message
    try:
        mq.send(message, block=False, type=13)
    except sysv_ipc.BusyError:
        print "Queue is full, ignoring"

def send_messages(mq, service_counter, status_counter, test_service):
    try:
        for key, item in test_service.iteritems():
            if type(item) == str:
                message = 'riold122^%s^%s^%s\0' % (key, status_counter, item)
                send_message(mq, message)
            elif type(item) == list:
                for msg in item:
                    message = 'riold122^%s^%s^%s\0' % (key, status_counter, msg)
                    send_message(mq, message)
    except Exception as excep:
        print excep, "Ignoring."
        pass


def main(test_service):
    DAT = open("fakenagios.dat", "w")
    scale_list = [1.0] #, 1100.0, 1200.0, 1300.0, 1400.0, 1500.0]
    period = 600
    mq = sysv_ipc.MessageQueue(123456, flags=sysv_ipc.IPC_CREAT, mode=0644)
    for scale in scale_list:
        check = True
        msg_counter = 0
        service_counter = status_counter = 0
        init_time = time.time()
        sleep_delta = 1 / scale
        print "Init scale %s" % scale
        print "Delta %s" % sleep_delta
        print "Period %s" % period
        while check:
            msg_init_time = time.time()
            try:
                now = datetime.datetime.fromtimestamp(time.time())
                messages_on_queue = mq.current_messages
                DAT.write("%s %d %d\n" % (now.strftime("%H:%M:%S"), scale,
                                          messages_on_queue))
                DAT.flush()
                # Send message
                send_messages(mq, service_counter, status_counter, test_service)
                status_counter = (status_counter + 1) % 4
                if status_counter == 0:
                    service_counter = (service_counter + 1) % 8
                # Calc time to sleep
                msg_counter = msg_counter + 1
                now = time.time()
                sleep_time = sleep_delta - (now - msg_init_time)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                if  now > init_time + period:
                    print ">>>>> Sent %s messages. Average of %s per sec" % \
                          (msg_counter, str(msg_counter / (now - init_time)))
                    check = False
            except KeyboardInterrupt:
                DAT.close()
                print "User interrupted. Shutting down."
                exit(0)
            except sysv_ipc.ExistentialError:
                print "Message queue does not exist for key"
                exit(1)
    DAT.close()
