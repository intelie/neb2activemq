#coding: utf-8
import unittest
import sys
import cStringIO
sys.path.append('../nebpublisher')
import manager


class MockQueue(object):
    def __init__(self, header, body):
        self.header = header
        self.body = body

    def get(self, something=True):
        return self.header, self.body


class MockLogger(object):
    def debug(self, message):
        print('DEBUG: %s' % message)


    def info(self, message):
        print('INFO: %s' % message) # or sys.stdout.write(msg + '\n')


    def error(self, message):
        sys.stderr.write('ERROR: %s\n' % message)


class MockConnectionAdapter(object):
    def __init__(self, settings, delay):
        self.sent_messages = 0


    def send(self, message, header, destination):
        print('Send message = "%s", header = "%s", destination: = "%s"' % \
              (str(message), header, str(destination)))
        self.sent_messages += 1


class TestQueueProcessor(unittest.TestCase):
    def test_queue_processor_send_one_message_without_UnicodeDecodeError(self):
        body = {'foo': 'bar'}
        queue = MockQueue(header={'destination': 123}, body=body)
        settings = type('bar', tuple(), {})
        settings.BROKER = None
        settings.CONN_SLEEP_DELAY = None
        manager.ConnectionAdapter = MockConnectionAdapter
        queue_processor = manager.QueueProcessor(queue, settings)
        manager.logger = MockLogger()
        queue_processor.process(max_messages=1)
        self.assertEqual(1, queue_processor.connection.sent_messages)


    def test_queue_processor_send_no_message_if_UnicodeDecodeError(self):
        body = {'foo': u"\u4561", 'bar': '✓', 'baz': "\x81"}
        queue = MockQueue(header={'destination': 123}, body=body)
        settings = type('bar', tuple(), {})
        settings.BROKER = None
        settings.CONN_SLEEP_DELAY = None
        manager.ConnectionAdapter = MockConnectionAdapter
        queue_processor = manager.QueueProcessor(queue, settings)
        manager.logger = MockLogger()
        queue_processor.process(max_messages=1)
        self.assertEqual(0, queue_processor.connection.sent_messages)


    def test_mock_queue(self):
        header = 'bla bla bla'
        body = 'something'
        q = MockQueue(header, body)
        header_from_queue, body_from_queue = q.get(True)
        self.assertEqual(header, header_from_queue)
        self.assertEqual(body, body_from_queue)


    def test_logger_debug(self):
        logger = MockLogger()
        stdout = cStringIO.StringIO()
        old_stdout = sys.stdout
        sys.stdout = stdout
        logger.debug('test')
        self.assertEqual(stdout.getvalue(), 'DEBUG: test\n')
        sys.stdout = old_stdout
        stdout.close()


    def test_logger_info(self):
        logger = MockLogger()
        stdout = cStringIO.StringIO()
        old_stdout = sys.stdout
        sys.stdout = stdout
        logger.info('test')
        self.assertEqual(stdout.getvalue(), 'INFO: test\n')
        sys.stdout = old_stdout
        stdout.close()


    def test_logger_error(self):
        logger = MockLogger()
        stderr = cStringIO.StringIO()
        old_stderr = sys.stderr
        sys.stderr = stderr
        logger.error('test')
        self.assertEqual(stderr.getvalue(), 'ERROR: test\n')
        sys.stderr = old_stderr
        stderr.close()


if __name__ == '__main__':
    unittest.main()

