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
        message = 'somehost^2^FPING CRITICAL - 201.59.129.13 (loss=100% )'
        #TODO: verify what string Nagios send on host check
        result = self.parser.parse(14, message)
        self.assertTrue(result != BAD_FORMAT)
        self.assertTrue(result != NOT_IMPLEMENTED)
        self.assertEqual('100', result[0]['loss'])
        self.assertEqual('UNKNOWN', result[0]['state'])
        self.assertEqual('somehost', result[0]['host'])
        self.assertEqual('PING', result[0]['eventtype'])
        self.assertEqual('201.59.129.13', result[0]['ip'])

    def test_host_check_ok(self):
        message = 'somehost^0^FPING OK - 200.225.157.77 (loss=0%, rta=0.690000 ms)'
        #TODO: verify what string Nagios send on host check
        result = self.parser.parse(14, message)
        self.assertTrue(result != BAD_FORMAT)
        self.assertTrue(result != NOT_IMPLEMENTED)
        self.assertEqual('0', result[0]['loss'])
        self.assertEqual('0.690000', result[0]['rta'])
        self.assertEqual('200.225.157.77', result[0]['ip'])
        self.assertEqual('OK', result[0]['state'])
        self.assertEqual('somehost', result[0]['host'])
        self.assertEqual('PING', result[0]['eventtype'])

    def test_host_check_parse_error(self):
        message = 'host^0^some message'
        result = self.parser.parse(14, message)
        self.assertTrue(result == BAD_FORMAT)        

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
    
    
    def test_check_unix_df_empty(self):
        message = 'some_host^check_unix_df^0^DISK OK'
        events = self.parser.parse_service_check(message)
        self.assertTrue(type(events) != type(42))
        self.assertEqual(1, len(events))
        event = events[0]
        self.assertTrue(type(event) != type(42))
        self.assertEqual('Disk', event['eventtype'])
        self.assertEqual('OK', event['state'])
        self.assertEqual('some_host', event['host'])


    def test_check_unix_df_one_partition(self):
        message = 'some_host^check_unix_df^0^DISK OK [1463088 kB (74%) free on /]'
        events = self.parser.parse_service_check(message)
        self.assertTrue(type(events) != type(42))
        self.assertEqual(1, len(events))
        event = events[0]
        self.assertTrue(type(event) != type(42))
        self.assertEqual('Disk', event['eventtype'])
        self.assertEqual('OK', event['state'])
        self.assertEqual('some_host', event['host'])
        self.assertEqual('/', event['partition'])
        self.assertEqual(74, event['free_percent'])


    def test_check_unix_df_one_partition(self):
        message = 'some_host^check_unix_df^0^DISK OK [1463088 kB (74%) free on /] [161576 kB (84%) free on /boot] [8207240 kB (100%) free on /dev/shm] [3630536 kB (74%) free on /home] [340256896 kB (91%) free on /iG] [1890652 kB (96%) free on /tmp] [3680220 kB (75%) free on /usr] [3596540 kB (73%) free on /var] [250298192 kB (20%) free on /u01] [1342944384 kB (68%) free on /u02]'
        events = self.parser.parse_service_check(message)
        self.assertTrue(type(events) != type(42))
        self.assertEqual(10, len(events))
        
        #[1463088 kB (74%) free on /]
        self.assertTrue(type(events[0]) != type(42))
        self.assertEqual('Disk', events[0]['eventtype'])
        self.assertEqual('OK', events[0]['state'])
        self.assertEqual('some_host', events[0]['host'])
        self.assertEqual('/', events[0]['partition'])
        self.assertEqual(74.0, events[0]['free_percent'])

        #[161576 kB (84%) free on /boot]
        self.assertTrue(type(events[1]) != type(42))
        self.assertEqual('Disk', events[1]['eventtype'])
        self.assertEqual('OK', events[1]['state'])
        self.assertEqual('some_host', events[1]['host'])
        self.assertEqual('/boot', events[1]['partition'])
        self.assertEqual(84.0, events[1]['free_percent'])

        #[8207240 kB (100%) free on /dev/shm]
        self.assertTrue(type(events[2]) != type(42))
        self.assertEqual('Disk', events[2]['eventtype'])
        self.assertEqual('OK', events[2]['state'])
        self.assertEqual('some_host', events[2]['host'])
        self.assertEqual('/dev/shm', events[2]['partition'])
        self.assertEqual(100.0, events[2]['free_percent'])

        #[3630536 kB (74%) free on /home]
        self.assertTrue(type(events[3]) != type(42))
        self.assertEqual('Disk', events[3]['eventtype'])
        self.assertEqual('OK', events[3]['state'])
        self.assertEqual('some_host', events[3]['host'])
        self.assertEqual('/home', events[3]['partition'])
        self.assertEqual(74.0, events[3]['free_percent'])

        #[340256896 kB (91%) free on /iG]
        self.assertTrue(type(events[4]) != type(42))
        self.assertEqual('Disk', events[4]['eventtype'])
        self.assertEqual('OK', events[4]['state'])
        self.assertEqual('some_host', events[4]['host'])
        self.assertEqual('/iG', events[4]['partition'])
        self.assertEqual(91.0, events[4]['free_percent'])

        #[1890652 kB (96%) free on /tmp]
        self.assertTrue(type(events[5]) != type(42))
        self.assertEqual('Disk', events[5]['eventtype'])
        self.assertEqual('OK', events[5]['state'])
        self.assertEqual('some_host', events[5]['host'])
        self.assertEqual('/tmp', events[5]['partition'])
        self.assertEqual(96.0, events[5]['free_percent'])

        #[3680220 kB (75%) free on /usr]
        self.assertTrue(type(events[6]) != type(42))
        self.assertEqual('Disk', events[6]['eventtype'])
        self.assertEqual('OK', events[6]['state'])
        self.assertEqual('some_host', events[6]['host'])
        self.assertEqual('/usr', events[6]['partition'])
        self.assertEqual(75.0, events[6]['free_percent'])

        #[3596540 kB (73%) free on /var]
        self.assertTrue(type(events[7]) != type(42))
        self.assertEqual('Disk', events[7]['eventtype'])
        self.assertEqual('OK', events[7]['state'])
        self.assertEqual('some_host', events[7]['host'])
        self.assertEqual('/var', events[7]['partition'])
        self.assertEqual(73.0, events[7]['free_percent'])

        #[250298192 kB (20%) free on /u01]
        self.assertTrue(type(events[8]) != type(42))
        self.assertEqual('Disk', events[8]['eventtype'])
        self.assertEqual('OK', events[8]['state'])
        self.assertEqual('some_host', events[8]['host'])
        self.assertEqual('/u01', events[8]['partition'])
        self.assertEqual(20.0, events[8]['free_percent'])

        #[1342944384 kB (68%) free on /u02]
        self.assertTrue(type(events[9]) != type(42))
        self.assertEqual('Disk', events[9]['eventtype'])
        self.assertEqual('OK', events[9]['state'])
        self.assertEqual('some_host', events[9]['host'])
        self.assertEqual('/u02', events[9]['partition'])
        self.assertEqual(68.0, events[9]['free_percent'])


    def test_check_unix_df_other_format(self):
        message = 'some_host^check_unix_df^0^DISK OK - free space: / 1096 MB (57% inode=95%): /tmp 2801 MB (97% inode=99%): /iG 735192 MB (94% inode=97%): /home 4410 MB (96% inode=99%): /usr 3482 MB (72% inode=88%): /var 3886 MB (81% inode=97%): /boot 137 MB (73% inode=99%): /dev/shm 16093 MB (100% inode=99%): /iG/dominios/publicador_arqs77 815668 MB (62% inode=94%):'
        events = self.parser.parse_service_check(message)

        self.assertEqual(9, len(events))
        for event in events:
            self.assertEqual('some_host', event['host'])
            self.assertEqual('OK', event['state'])
            self.assertEqual('Disk', event['eventtype'])

            #/ 1096 MB (57% inode=95%):
            self.assertEqual('/', events[0]['partition'])
            self.assertEqual(57.0, events[0]['free_percent'])

            #/tmp 2801 MB (97% inode=99%):
            self.assertEqual('/tmp', events[1]['partition'])
            self.assertEqual(97.0, events[1]['free_percent'])

            #/iG 735192 MB (94% inode=97%):
            self.assertEqual('/iG', events[2]['partition'])
            self.assertEqual(94.0, events[2]['free_percent'])

            #/home 4410 MB (96% inode=99%):
            self.assertEqual('/home', events[3]['partition'])
            self.assertEqual(96.0, events[3]['free_percent'])

            #/usr 3482 MB (72% inode=88%):
            self.assertEqual('/usr', events[4]['partition'])
            self.assertEqual(72.0, events[4]['free_percent'])

            #/var 3886 MB (81% inode=97%):
            self.assertEqual('/var', events[5]['partition'])
            self.assertEqual(81.0, events[5]['free_percent'])

            #/boot 137 MB (73% inode=99%):
            self.assertEqual('/boot', events[6]['partition'])
            self.assertEqual(73.0, events[6]['free_percent'])

            #/dev/shm 16093 MB (100% inode=99%):
            self.assertEqual('/dev/shm', events[7]['partition'])
            self.assertEqual(100.0, events[7]['free_percent'])

            #/iG/dominios/publicador_arqs77 815668 MB (62% inode=94%):
            self.assertEqual('/iG/dominios/publicador_arqs77', events[8]['partition'])
            self.assertEqual(62.0, events[8]['free_percent'])

    def test_check_unix_df_problem(self):
        message = 'some_host^check_unix_df^1^DISK WARNING [1551620 kB (79%) free on /dev/mapper/Vol_IG-root_lv] [170506 kB (88%) free on /dev/sda1] [8207240 kB (100%) free on /dev/shm] [3197896 kB (65%) free on /dev/mapper/Vol_IG-home_lv] [88741864 kB (23%) free on /dev/mapper/Vol_IG-ig_lv] [1890660 kB (96%) free on /dev/mapper/Vol_IG-tmp_lv] [3713612 kB (75%) free on /dev/mapper/Vol_IG-usr_lv] [3652340 kB (74%) free on /dev/mapper/Vol_IG-var_lv] [228675264 kB (18%) free on /dev/mapper/AMSFC-u01FC] [186979120 kB (9%)'
        events = self.parser.parse_service_check(message)
        self.assertEqual(9, len(events))

    def test_check_unix_df_warning(self):
        message = 'some_host^check_unix_df^1^DISK WARNING [94573136 kB (90%) used on /dev/mapper/Vol_IG-ig_lv]'
        events = self.parser.parse_service_check(message)
        self.assertEqual(1, len(events))
        event = events[0]
        self.assertEqual('some_host', event['host'])
        self.assertEqual('WARNING', event['state'])
        self.assertEqual('Disk', event['eventtype'])
        self.assertEqual('/dev/mapper/Vol_IG-ig_lv', event['partition'])
        self.assertEqual(10.0, event['free_percent'])

    def test_check_event_log(self):
        message = 'some_host^check_log^4^2010-11-12 09:53:57.614 ERROR [2480] - Error on line 14 of monitor MyMonitor (monitors\MyMonitor.mon): Invalid key "a" passed to dictionary [] operator'
        events = self.parser.parse_service_check(message)
        self.assertEqual(1, len(events))
        event = events[0]
        self.assertEqual('some_host', event['host'])
        self.assertEqual('ERROR', event['state'])
        self.assertEqual('check_log', event['eventtype'])
        self.assertEqual('2010-11-12 09:53:57.614', event['log_time'])
        self.assertEqual('2480', event['error_code'])
        self.assertEqual('Error on line 14 of monitor MyMonitor (monitors\MyMonitor.mon): Invalid key "a" passed to dictionary [] operator', event['log_line'])


if __name__ == '__main__':
    unittest.main()
