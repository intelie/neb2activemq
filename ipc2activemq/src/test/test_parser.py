import sys
import unittest
import imp

sys.path.append('../../')
from src.nebpublisher.utils.parser import *

class TestServiceParser(unittest.TestCase):
    def setUp(self):
        #TODO: make it more extensible
        topics_path = '../nebpublisher/conf/prod/'
        topics = imp.load_source("topics", topics_path, open(topics_path+'topics.py', 'rb'))
        
        parser_functions_path = '../nebpublisher/conf/prod/'
        parser_functions = imp.load_source("parser_functions", parser_functions_path, open(parser_functions_path+'parser_functions.py', 'rb'))
        self.parser = Parser(topics, parser_functions)

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
    def test_check_cpu(self):
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

    def test_check_disk(self):
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

    def test_check_load(self):
        message = "riold122^check_load^0^Load average OK - 0 0 0 | iso.3.6.1.4.1.2021.10.1.3.1=0 iso.3.6.1.4.1.2021.10.1.3.2=0 iso.3.6.1.4.1.2021.10.1.3.3=0"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "OK")
        self.assertEqual(events[0]["min1"], "0")
        self.assertEqual(events[0]["min5"], "0")
        self.assertEqual(events[0]["min15"], "0")
        self.assertEqual(events[0]["eventtype"], "Load")
        
        message = "riold122^check_load^0^Load average WARNING - *1* 0 1 | iso.3.6.1.4.1.2021.10.1.3.1=1 iso.3.6.1.4.1.2021.10.1.3.2=0 iso.3.6.1.4.1.2021.10.1.3.3=1"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "WARNING")
        self.assertEqual(events[0]["min1"], "1")
        self.assertEqual(events[0]["min5"], "0")
        self.assertEqual(events[0]["min15"], "1")

        message = "riold122^check_load^0^Load average CRITICAL - *1* 0 1 | iso.3.6.1.4.1.2021.10.1.3.1=1 iso.3.6.1.4.1.2021.10.1.3.2=0 iso.3.6.1.4.1.2021.10.1.3.3=1"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")
        self.assertEqual(events[0]["min1"], "1")
        self.assertEqual(events[0]["min5"], "0")
        self.assertEqual(events[0]["min15"], "1")

    def test_check_swap(self):
        message = "riold122^check_swap^0^Swap OK - 16780208 kB total size ( 16780112 kB available space) | iso.3.6.1.4.1.2021.4.3.0=16780208 iso.3.6.1.4.1.2021.4.4.0=16780112"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "OK")
        self.assertEqual(events[0]["total"], "16780208")
        self.assertEqual(events[0]["available"], "16780112")
        self.assertEqual(events[0]["eventtype"], "Swap")
        
        message = "riold122^check_swap^0^Swap WARNING - 16780208 kB total size ( *16780112* kB available space) | iso.3.6.1.4.1.2021.4.3.0=16780208 iso.3.6.1.4.1.2021.4.4.0=16780112"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "WARNING")
        self.assertEqual(events[0]["total"], "16780208")
        self.assertEqual(events[0]["available"], "16780112")

        message = "riold122^check_swap^0^Swap CRITICAL - 16780208 kB total size ( *16780112* kB available space) | iso.3.6.1.4.1.2021.4.3.0=16780208 iso.3.6.1.4.1.2021.4.4.0=16780112"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")
        self.assertEqual(events[0]["total"], "16780208")
        self.assertEqual(events[0]["available"], "16780112")

    def test_check_http(self):
        message = "riold122^check_http^0^HTTP OK HTTP/1.1 200 OK - 0.001 second response time |time=0.001378s;;;0.000000 size=259B;;;00"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "OK")
        self.assertEqual(events[0]["status_code"], "200")
        self.assertEqual(events[0]["response_time"], "0.001")
        self.assertEqual(events[0]["eventtype"], "HTTP")
        
        message = "riold122^check_http^0^HTTP OK - HTTP/1.1 301 Moved Permanently - 0.002 second response time"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "OK")
        self.assertEqual(events[0]["status_code"], "301")
        self.assertEqual(events[0]["response_time"], "0.002")

        message = "riold122^check_http^0^HTTP OK - HTTP/1.1 302 Moved Temporarily - 0.000 second response time"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "OK")
        self.assertEqual(events[0]["status_code"], "302")
        self.assertEqual(events[0]["response_time"], "0.000")

        message = "riold122^check_http^0^HTTP OK - HTTP/1.1 302 Found - 0.005 second response time"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "OK")
        self.assertEqual(events[0]["status_code"], "302")
        self.assertEqual(events[0]["response_time"], "0.005")

        message = "riold122^check_http^0^HTTP OK - HTTP/1.1 302 Object moved - 0.009 second response time"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "OK")
        self.assertEqual(events[0]["status_code"], "302")
        self.assertEqual(events[0]["response_time"], "0.009")

        message = "riold122^check_http^0^HTTP WARNING: HTTP/1.1 400 Bad Request"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "WARNING")
        self.assertEqual(events[0]["status_code"], "400")

        message = "riold122^check_http^0^HTTP WARNING: HTTP/1.1 403 Forbidden"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "WARNING")
        self.assertEqual(events[0]["status_code"], "403")

        message = "riold122^check_http^0^HTTP WARNING: HTTP/1.1 404 Not Found"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "WARNING")
        self.assertEqual(events[0]["status_code"], "404")

        message = "riold122^check_http^0^HTTP WARNING: HTTP/1.1 404 NOT FOUND"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "WARNING")
        self.assertEqual(events[0]["status_code"], "404")

        message = "riold122^check_http^0^HTTP WARNING: HTTP/1.1 404 Object Not Found"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "WARNING")
        self.assertEqual(events[0]["status_code"], "404")

        message = "riold122^check_http^0^HTTP CRITICAL: HTTP/1.1 500 Internal Server Error"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")
        self.assertEqual(events[0]["status_code"], "500")

        message = "riold122^check_http^0^HTTP CRITICAL: HTTP/1.1 500 INTERNAL SERVER ERRORe"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")
        self.assertEqual(events[0]["status_code"], "500")

        message = "riold122^check_http^0^HTTP CRITICAL: HTTP/1.1 500 Server Error"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")
        self.assertEqual(events[0]["status_code"], "500")

        message = "riold122^check_http^0^HTTP CRITICAL: HTTP/1.1 502 Proxy Error"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")
        self.assertEqual(events[0]["status_code"], "502")

        message = "riold122^check_http^0^HTTP CRITICAL: HTTP/1.1 503 Service Temporarily Unavailable"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")
        self.assertEqual(events[0]["status_code"], "503")

        message = "riold122^check_http^0^HTTP CRITICAL: HTTP/1.1 503 Service Unavailable"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")
        self.assertEqual(events[0]["status_code"], "503")
				
        message = "riold122^check_http^0^CRITICAL - Socket timeout after 5 seconds"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")

        message = "riold122^check_http^0^HTTP CRITICAL - string not found|time=0.001627s;;;0.000000 size=259B;;;0"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")

    def test_check_fping(self):
        message = "riold122^check_fping^0^FPING OK - riosf109.globoi.com (loss=0%, rta=0.560000 ms)|loss=0%;;;0;100 rta=0.000560s;;;0.000000"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "OK")
        self.assertEqual(events[0]["loss"], "0")
        self.assertEqual(events[0]["rta"], "0.560000")
        self.assertEqual(events[0]["eventtype"], "FPING")
        
        message = "riold122^check_fping^0^FPING CRITICAL - riolf95.globoi.com (loss=100% )|loss=100%;;;0;100"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")
        self.assertEqual(events[0]["loss"], "100")

    def test_check_tcp(self):
        message = "riold122^check_tcp^0^TCP OK - 0.092 second response time on port 3737"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["description"], "TCP OK - 0.092 second response time on port 3737")
        self.assertEqual(events[0]["state"], "OK")
        self.assertEqual(events[0]["response_time"], "0.092")
        self.assertEqual(events[0]["port"], "3737")
        self.assertEqual(events[0]["eventtype"], "TCP")
        
        message = "riold122^check_tcp^0^TCP OK - 0.007 second response time on port 80|time=0.007330s;;;0.000000;10.000000"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "OK")
        self.assertEqual(events[0]["response_time"], "0.007")
        self.assertEqual(events[0]["port"], "80")

        message = "riold122^check_tcp^0^CRITICAL - Socket timeout after 10 seconds"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")

        message = "riold122^check_tcp^0^TCP CRITICAL - Invalid hostname, address or socket: puppet02.globoi.com"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")

    def test_memcached_hit(self):
        message = "riold122^check_memcached_hit^0^MEMCACHED OK - OK, Hit checked: OK - at 10.10.48.4:11211"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "OK")
        self.assertEqual(events[0]["description"], "MEMCACHED OK - OK, Hit checked: OK - at 10.10.48.4:11211")
        self.assertEqual(events[0]["eventtype"], "MemCachedHit")
        
        message = "riold122^check_memcached_hit^0^MEMCACHED WARNING - Hit checked: NG - at 10.10.245.9:11211 | hits=83.67[%];@6:90;@6"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "WARNING")
        self.assertEqual(events[0]["hits"], "83.67")
        self.assertEqual(events[0]["description"], "MEMCACHED WARNING - Hit checked: NG - at 10.10.245.9:11211 | hits=83.67[%];@6:90;@6")
        self.assertEqual(events[0]["eventtype"], "MemCachedHit")
        
        message = "riold122^check_memcached_hit^0^MEMCACHED CRITICAL - Hit checked: NG - at 10.10.245.9:11211 | hits=83.67[%];@85:90;@85"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")
        self.assertEqual(events[0]["hits"], "83.67")
        self.assertEqual(events[0]["description"], "MEMCACHED CRITICAL - Hit checked: NG - at 10.10.245.9:11211 | hits=83.67[%];@85:90;@85")
        self.assertEqual(events[0]["eventtype"], "MemCachedHit")
        
        message = "riold122^check_memcached_hit^0^MEMCACHED CRITICAL - Cant connect to 10.10.237.53"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")
        self.assertEqual(events[0]["description"], "MEMCACHED CRITICAL - Cant connect to 10.10.237.53")
        self.assertEqual(events[0]["eventtype"], "MemCachedHit")
        
    def test_memcached_size(self):
        message = "riold122^check_memcached_size^0^MEMCACHED OK - OK, Size checked: OK - at 10.10.245.10:11211"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "OK")
        self.assertEqual(events[0]["description"], "MEMCACHED OK - OK, Size checked: OK - at 10.10.245.10:11211")
        self.assertEqual(events[0]["eventtype"], "MemCachedSize")
        
        message = "riold122^check_memcached_size^0^MEMCACHED WARNING - Size checked: NG - at 10.10.245.9:11211 | size=7.64[%];6;80"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "WARNING")
        self.assertEqual(events[0]["size"], "7.64")
        self.assertEqual(events[0]["description"], "MEMCACHED WARNING - Size checked: NG - at 10.10.245.9:11211 | size=7.64[%];6;80")
        self.assertEqual(events[0]["eventtype"], "MemCachedSize")
        
        message = "riold122^check_memcached_size^0^MEMCACHED CRITICAL - Size checked: NG - at 10.10.245.9:11211 | size=7.64[%];5;6"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")
        self.assertEqual(events[0]["size"], "7.64")
        self.assertEqual(events[0]["description"], "MEMCACHED CRITICAL - Size checked: NG - at 10.10.245.9:11211 | size=7.64[%];5;6")
        self.assertEqual(events[0]["eventtype"], "MemCachedSize")
        
        message = "riold122^check_memcached_size^0^MEMCACHED CRITICAL - Can't connect to 10.10.245.12"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")
        self.assertEqual(events[0]["description"], "MEMCACHED CRITICAL - Can't connect to 10.10.245.12")
        self.assertEqual(events[0]["eventtype"], "MemCachedSize")

    def test_check_mysql_health_connection_time(self):
        message = "riold122^check_mysql_health_connection_time^0^OK - 0.04 seconds to connect as usr_nagios"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "OK")
        self.assertEqual(events[0]["seconds"], "0.04")
        self.assertEqual(events[0]["user"], "usr_nagios")
        self.assertEqual(events[0]["description"], "OK - 0.04 seconds to connect as usr_nagios")
        self.assertEqual(events[0]["eventtype"], "MysqlHealthConnectionTime")

        message = "riold122^check_mysql_health_connection_time^0^WARNING - 0.02 seconds to connect as nagiosql | connection_time=0.0234s;0;5"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "WARNING")
        self.assertEqual(events[0]["seconds"], "0.02")
        self.assertEqual(events[0]["user"], "nagiosql")
        self.assertEqual(events[0]["description"], "WARNING - 0.02 seconds to connect as nagiosql | connection_time=0.0234s;0;5")
        self.assertEqual(events[0]["eventtype"], "MysqlHealthConnectionTime")
        
        message = "riold122^check_mysql_health_connection_time^0^CRITICAL - 0.02 seconds to connect as nagiosql | connection_time=0.0239s;1;0"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")
        self.assertEqual(events[0]["seconds"], "0.02")
        self.assertEqual(events[0]["user"], "nagiosql")
        self.assertEqual(events[0]["description"], "CRITICAL - 0.02 seconds to connect as nagiosql | connection_time=0.0239s;1;0")
        self.assertEqual(events[0]["eventtype"], "MysqlHealthConnectionTime")
        
    def test_check_mysql_health_slow_queries(self):
        message = "riold122^check_mysql_health_slow_queries^0^OK - 0 slow queries in 1024 seconds (0.00/sec)"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "OK")
        self.assertEqual(events[0]["count"], "0")
        self.assertEqual(events[0]["window"], "1024")
        self.assertEqual(events[0]["description"], "OK - 0 slow queries in 1024 seconds (0.00/sec)")
        self.assertEqual(events[0]["eventtype"], "MysqlHealthSlowQueries")
        
    def test_check_mysql_health_slave_lag(self):
        message = "riold122^check_mysql_health_slave-lag^0^OK - Slave is 10 seconds behind master"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "OK")
        self.assertEqual(events[0]["seconds"], "10")
        self.assertEqual(events[0]["description"], "OK - Slave is 10 seconds behind master")
        self.assertEqual(events[0]["eventtype"], "MysqlHealthSlaveLag")
        
        message = "riold122^check_mysql_health_slave-lag^0^WARNING - Slave is 12 seconds behind master"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "WARNING")
        self.assertEqual(events[0]["seconds"], "12")
        self.assertEqual(events[0]["description"], "WARNING - Slave is 12 seconds behind master")
        self.assertEqual(events[0]["eventtype"], "MysqlHealthSlaveLag")
        
        message = "riold122^check_mysql_health_slave-lag^0^CRITICAL - Slave is 87 seconds behind master"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")
        self.assertEqual(events[0]["seconds"], "87")
        self.assertEqual(events[0]["description"], "CRITICAL - Slave is 87 seconds behind master")
        self.assertEqual(events[0]["eventtype"], "MysqlHealthSlaveLag")
         
    def test_check_mysql_health_threads_connected(self):
       message = "riold122^check_mysql_health_threads_connected^0^OK - 3 client connection threads"
       events = self.parser.parse_service_check(message)
       self.assertEqual(events[0]["state"], "OK")
       self.assertEqual(events[0]["count"], "3")
       self.assertEqual(events[0]["description"], "OK - 3 client connection threads")
       self.assertEqual(events[0]["eventtype"], "MysqlHealthThreadsConnected") 
      
       message = "riold122^check_mysql_health_threads_connected^0^WARNING - 100 client connection threads"
       events = self.parser.parse_service_check(message)
       self.assertEqual(events[0]["state"], "WARNING")
       self.assertEqual(events[0]["count"], "100")
       self.assertEqual(events[0]["description"], "WARNING - 100 client connection threads")
       self.assertEqual(events[0]["eventtype"], "MysqlHealthThreadsConnected")
       
       message = "riold122^check_mysql_health_threads_connected^0^CRITICAL - 129 client connection threads"
       events = self.parser.parse_service_check(message)
       self.assertEqual(events[0]["state"], "CRITICAL")
       self.assertEqual(events[0]["count"], "129")
       self.assertEqual(events[0]["description"], "CRITICAL - 129 client connection threads")
       self.assertEqual(events[0]["eventtype"], "MysqlHealthThreadsConnected")
         
    def test_check_mysql_health_slave_io_running(self):
        message = "riold122^check_mysql_health_slave-io-running^0^OK - Slave io is running"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "OK")
        self.assertEqual(events[0]["description"], "OK - Slave io is running")
        self.assertEqual(events[0]["eventtype"], "MysqlHealthSlaveIORunning")

    def test_check_mysql_health_slave_sql_running(self):
        message = "riold122^check_mysql_health_slave-sql-running^0^OK - Slave sql is running"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "OK")
        self.assertEqual(events[0]["description"], "OK - Slave sql is running")
        self.assertEqual(events[0]["eventtype"], "MysqlHealthSlaveSqlRunning")

    def test_check_memory(self):
        message = "riold122^check_memory^0^Memory RAM OK - 9005560 kB free ( 17198668 kB used) | iso.3.6.1.4.1.2021.4.6.0=9005560 iso.3.6.1.4.1.2021.4.11.0=17198668"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "OK")
        self.assertEqual(events[0]["eventtype"], "Memory")
    #    self.assertEqual(events[0]["free"], "9005560")
     #   self.assertEqual(events[0]["used"], "17198668")

    def test_check_passive(self):
      message = "riold122^check_passive^0^cameras gcom/live:1 gnews/live:34 gsat/live1:0 gsat/live2:0 gsat/live3:0 g1rj1/live:0 g1sp1/live:89 bbb/pgma:569 bbb/pgmb:478 bbb/cam1:2 bbb/cam2:10 bbb/cam3:5 bbb/cam4:8 bbb/cam5:19 chat/dwt:0 chat/pjc:3 chat/ber1:1 chat/ber2:0 chat/cgj:0"
      events = self.parser.parse_service_check(message)
      self.assertEqual(events[0]["eventtype"], "FMS")
      self.assertEqual(events[0]["label"], "gcom/live")
      self.assertEqual(events[0]["value"], "1")
      
      self.assertEqual(events[1]["eventtype"], "FMS")
      self.assertEqual(events[1]["label"], "gnews/live")
      self.assertEqual(events[1]["value"], "34")
      
    # Test expected errors
    def test_error_checks_mysql(self):
        message = "riold122^check_mysql_health_slave-sql-running^0^CRITICAL - cannot connect to information_schema. Can't connect to MySQL server on '10.10.138.49' (111)"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")
        self.assertEqual(events[0]["description"], "CRITICAL - cannot connect to information_schema. Can't connect to MySQL server on '10.10.138.49' (111)")
        self.assertEqual(events[0]["eventtype"], "MysqlCannotConnect") 

        message = "riold122^check_mysql_health_connection_time^0^CRITICAL - cannot connect to information_schema. Access denied for user nagios@10.10.5.42 (using password: YES)"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")
        self.assertEqual(events[0]["description"], "CRITICAL - cannot connect to information_schema. Access denied for user nagios@10.10.5.42 (using password: YES)")
        self.assertEqual(events[0]["eventtype"], "MysqlCannotConnect")
        
        message = "riold122^check_mysql_health_slow_queries^0^CRITICAL - cannot connect to information_schema. Too many connections"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")
        self.assertEqual(events[0]["description"], "CRITICAL - cannot connect to information_schema. Too many connections")
        self.assertEqual(events[0]["eventtype"], "MysqlCannotConnect")
        
        message = "riold122^check_mysql_health_slave-lag^0^CRITICAL - connection could not be established within 60 seconds"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")
        self.assertEqual(events[0]["description"], "CRITICAL - connection could not be established within 60 seconds")
        self.assertEqual(events[0]["eventtype"], "MysqlCannotConnect")
        
        message = "riold122^check_mysql_health_threads_connected^0^CRITICAL - Socket timeout after 5 seconds"
        events = self.parser.parse_service_check(message)
        self.assertEqual(events[0]["state"], "CRITICAL")
        self.assertEqual(events[0]["description"], "CRITICAL - Socket timeout after 5 seconds")
        self.assertEqual(events[0]["eventtype"], "MysqlCannotConnect")
        
if __name__ == '__main__':
    unittest.main()
