import Queue
import threading
import sys
import imp
import time
from threading import Thread

MAXSIZE = 1000

class TestServiceParser(object):
    def __init__(self):
        self.queue = Queue.Queue(MAXSIZE)
        self.test_read_write()

    def test_read_write(self):
        self.a = {'a1': 1, 'a2': 2, 'a3': 'test'}
        self.b = {'b1': 1, 'b2': 2, 'b3': 'test'}

        try:
            self.writer = Writer(self.queue, self.a, self.b).start()
            self.reader = Reader(self.queue, self.a, self.b).start()
        except KeyboardInterrupt:
            self.writer.stop()
            self.reader.stop()
            print "User interrupted. Shutting down."
            exit(0)


class Writer(threading.Thread):
    def __init__ (self, queue, a, b):
        self.queue = queue
        self.a = a
        self.b = b
        threading.Thread.__init__(self)

    def run (self):
        while True:
            try:
                if self.queue.full():
                    self.queue.get_nowait()
                if not self.queue.full():
                    self.queue.put((str(self.a), str(self.b)))
                print "written: %s, %s" % (self.a, self.b)
                self.a['a1'] = self.a['a1'] + 1
                self.a['a2'] = self.a['a2'] + 1
                self.b['b1'] = self.b['b1'] + 1
                self.b['b2'] = self.b['b2'] + 1
                time.sleep(0.005)
            except KeyboardInterrupt:
                exit(0)


class Reader(threading.Thread):
    def __init__ (self, queue, a, b):
        self.queue = queue
        self.a = a
        self.b = b
        threading.Thread.__init__(self)

    def run (self):
        while True:
            try:
                a, b = self.queue.get(True)
                print "read: %s, %s" % (a, b)
            except Queue.Empty:
                print "Empty queue"
                continue
            except KeyboardInterrupt:
                exit(0)


if __name__ == '__main__':
    TestServiceParser()
