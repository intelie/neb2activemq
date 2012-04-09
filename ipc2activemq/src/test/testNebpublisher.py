import fakenagios
import sys
from mock import patch, MagicMock
import unittest
import time
from sysv_ipc import MessageQueue
import os

sys.path.append("..")
import ipc2activemq
from nebpublisher.connection_adapter import ConnectionAdapter

test_service = {
    'check_cpu': 'usage (%user %system %idle) OK - 0 0 99 | iso.3.6.1.4.1.2021.11.9.0=0 iso.3.6.1.4.1.2021.11.10.0=0 iso.3.6.1.4.1.2021.11.11.0=99',
}

class TestIPC2Activemq(unittest.TestCase):

    def test_message_integrity_and_if_nebpublisher_reads_from_the_queue(self):

        mq = MessageQueue(123456)
        with patch.object(ConnectionAdapter, '__init__') as mock_method:
            message = "Everything is Dust in the Wind"
            mq.send(message)
            mock_method.return_value = None
            mock_sender = ConnectionAdapter([('127.0.0.1', 61613)], 0)
            mock_sender.send = MagicMock()
            mock_sender.__connect = MagicMock(return_value=True)
            ipc2activemq.main()
            time.sleep(0.1)
            mock_sender.send.assert_called_with(message, None, None)
            assertEqual(0, mq.current_messages)

if __name__ == '__main__':
    unittest.main()
