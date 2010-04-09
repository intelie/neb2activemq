import sys
import unittest
import imp

sys.path.append('../../')
from src.nebpublisher.utils.neb_parser import *

class TestServiceParser(unittest.TestCase):
    def setUp(self):
        #TODO: make it more extensible
        topics_path = '../nebpublisher/conf/dev/'
        topics = imp.load_source("topics", topics_path, open(topics_path+'topics.py', 'rb'))
        
        parser_functions_path = '../nebpublisher/conf/dev/'
        parser_functions = imp.load_source("parser_functions", parser_functions_path, open(parser_functions_path+'parser_functions.py', 'rb'))
        self.parser = Parser(topics, parser_functions)

    def test_host_check_critical(self):
        message = 'somehost^FPING CRITICAL - 201.59.129.13 (loss=100% )'
        #TODO: verify what string Nagios send on host check
        result = self.parser.parse(14, message)
        self.assertTrue(result != BAD_FORMAT)
        self.assertEqual('100', result['loss'])
        self.assertEqual('CRITICAL', result['state'])
        self.assertEqual('somehost', result['host'])
        self.assertEqual('PING', result['eventtype'])
        self.assertEqual('201.59.129.13', result['ip'])

    def test_host_check_ok(self):
        message = 'somehost^FPING OK - 200.225.157.77 (loss=0%, rta=0.690000 ms)'
        #TODO: verify what string Nagios send on host check
        result = self.parser.parse(14, message)
        self.assertTrue(result != BAD_FORMAT)
        self.assertEqual('0', result['loss'])
        self.assertEqual('0.690000', result['rta'])
        self.assertEqual('200.225.157.77', result['ip'])
        self.assertEqual('OK', result['state'])
        self.assertEqual('somehost', result['host'])
        self.assertEqual('PING', result['eventtype'])


    # Test error cases
    def test_service_empty(self):
        result = self.parser.parse_service_check("")
        self.assertEqual(result, BAD_FORMAT)

    def test_service_none(self):
        result = self.parser.parse_service_check(None)
        self.assertEqual(result, BAD_FORMAT)

    def test_service_one_parameter(self):
        result = self.parser.parse_service_check("host")
        self.assertEqual(result, BAD_FORMAT)

    def test_service_empty_parameters(self):
        result = self.parser.parse_service_check("^^^")
        self.assertEqual(result, BAD_FORMAT)

    def test_service_empty_parameter1(self):
        result = self.parser.parse_service_check("^check_disk^0^Disk space OK - 8899052 kB free ( 39 % used)")
        self.assertEqual(result, BAD_FORMAT)    

    def test_create_event_wrong_state(self):
        result = self.parser.parse_service_check("hostname^FPING XXXX - srvvld48.test.com (loss=100% )")
        self.assertEqual(result, BAD_FORMAT)

    def test_create_event_wrong_free_space(self):
        result = self.parser.parse_service_check("riold122^check_disk^0^Disk space OK - XXXX kB free ( 39 % used)")
        self.assertEqual(result, BAD_FORMAT)

    def test_create_event_wrong_usage(self):
        result = self.parser.parse_service_check("riold122^check_disk^0^Disk space OK - 889 kB free ( XX % used)")
        self.assertEqual(result, BAD_FORMAT)

    def test_service_empty_parameter2(self):
        result = self.parser.parse_service_check("riold122^^0^Disk space OK - 8899052 kB free ( 39 % used)")
        self.assertEqual(result, BAD_FORMAT)

    def test_service_empty_parameter3(self):
        result = self.parser.parse_service_check("riold122^check_disk^^Disk space OK - 8899052 kB free ( 39 % used)")
        self.assertEqual(result, BAD_FORMAT)

    def test_service_empty_parameter4(self):
        result = self.parser.parse_service_check("riold122^check_disk^0^")
        self.assertEqual(result, BAD_FORMAT)
        
    def test_inexistant_topic(self):
        result = self.parser.parse_service_check("riold122^inexistant^0^CPU usage (%user %system %idle) OK - 0 0 99")
        self.assertEqual(result, BAD_FORMAT)

    # Test correct cases
    def GC_test_check_cpu(self):
        message = "riold122^check_cpu^0^CPU usage (%user %system %idle) OK - 0 0 99 | iso.3.6.1.4.1.2021.11.9.0=0 iso.3.6.1.4.1.2021.11.10.0=0 iso.3.6.1.4.1.2021.11.11.0=99"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "OK")
        self.assertEqual(events[0]["user"], "0")
        self.assertEqual(events[0]["system"], "0")
        self.assertEqual(events[0]["idle"], "99")
        self.assertEqual(events[0]["eventtype"], "CPU")

        message = "riold122^check_cpu^0^CPU usage (%user %system %idle) WARNING - 0 0 *99* | iso.3.6.1.4.1.2021.11.9.0=0 iso.3.6.1.4.1.2021.11.10.0=0 iso.3.6.1.4.1.2021.11.11.0=99"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "WARNING")
        self.assertEqual(events[0]["user"], "0")
        self.assertEqual(events[0]["system"], "0")
        self.assertEqual(events[0]["idle"], "99")
        self.assertEqual(events[0]["eventtype"], "CPU")
			
        message = "riold122^check_cpu^0^CPU usage (%user %system %idle) CRITICAL - 0 0 *99* | iso.3.6.1.4.1.2021.11.9.0=0 iso.3.6.1.4.1.2021.11.10.0=0 iso.3.6.1.4.1.2021.11.11.0=99"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")
        self.assertEqual(events[0]["user"], "0")
        self.assertEqual(events[0]["system"], "0")
        self.assertEqual(events[0]["idle"], "99")
        self.assertEqual(events[0]["eventtype"], "CPU")

    def GC_test_check_disk(self):
        message = "riold122^check_disk^0^Disk space OK - 64031408 kB free ( 3 % used) | iso.3.6.1.4.1.2021.9.1.7.1=64031408 iso.3.6.1.4.1.2021.9.1.9.1=3"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "OK")
        self.assertEqual(events[0]["free_space"], "64031408")
        self.assertEqual(events[0]["usage"], "3")
        self.assertEqual(events[0]["eventtype"], "Disk")

        message = "riold122^check_disk^0^Disk space WARNING - 64031408 kB free ( *3* % used) | iso.3.6.1.4.1.2021.9.1.7.1=64031408 iso.3.6.1.4.1.2021.9.1.9.1=3"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "WARNING")
        self.assertEqual(events[0]["free_space"], "64031408")
        self.assertEqual(events[0]["usage"], "3")

        message = "riold122^check_disk^0^Disk space CRITICAL - 64031408 kB free ( *3* % used) | iso.3.6.1.4.1.2021.9.1.7.1=64031408 iso.3.6.1.4.1.2021.9.1.9.1=3"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")
        self.assertEqual(events[0]["free_space"], "64031408")
        self.assertEqual(events[0]["usage"], "3")

        events = self.parser.parse_service_check("riold122^check_disk^0^Disk space OK - 8899052 kB free ( 39 % used)")
        self.assertEqual(events[0]["state"], "OK")
        self.assertEqual(events[0]["free_space"], "8899052")
        self.assertEqual(events[0]["usage"], "39")
        self.assertEqual(events[0]["eventtype"], "Disk")

    def test_check_passive(self):
      message = "riold122^check_passive^0^cameras gcom/live:1 gnews/live:34 gsat/live1:0 gsat/live2:0 gsat/live3:0 g1rj1/live:0 g1sp1/live:89 bbb/pgma:569 bbb/pgmb:478 bbb/cam1:2 bbb/cam2:10 bbb/cam3:5 bbb/cam4:8 bbb/cam5:19 chat/dwt:0 chat/pjc:3 chat/ber1:1 chat/ber2:0 chat/cgj:0"
      events = self.parser.parse_service_check(message)
      self.assertEqual(events[0]["eventtype"], "FMS")
      self.assertEqual(events[0]["label"], "gcom/live")
      self.assertEqual(events[0]["value"], "1")
      
      self.assertEqual(events[1]["eventtype"], "FMS")
      self.assertEqual(events[1]["label"], "gnews/live")
      self.assertEqual(events[1]["value"], "34")
      
        
if __name__ == '__main__':
    unittest.main()
