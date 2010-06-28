import fakenagios

test_service = {
    'check_cpu': 'usage (%user %system %idle) OK - 0 0 99 | iso.3.6.1.4.1.2021.11.9.0=0 iso.3.6.1.4.1.2021.11.10.0=0 iso.3.6.1.4.1.2021.11.11.0=99',
    'check_disk': 'Disk space OK - 64031408 kB free ( 3 % used) | iso.3.6.1.4.1.2021.9.1.7.1=64031408 iso.3.6.1.4.1.2021.9.1.9.1=3',
    'check_load': 'Load average OK - 0 0 0 | iso.3.6.1.4.1.2021.10.1.3.1=0 iso.3.6.1.4.1.2021.10.1.3.2=0 iso.3.6.1.4.1.2021.10.1.3.3=0',
    'check_swap': 'Swap OK - 16780208 kB total size ( 16780112 kB available space) | iso.3.6.1.4.1.2021.4.3.0=16780208 iso.3.6.1.4.1.2021.4.4.0=16780112',
    'check_http': 'HTTP OK HTTP/1.1 200 OK - 0.001 second response time |time=0.001378s;;;0.000000 size=259B;;;00',
    'check_fping': 'FPING OK - riosf109.globoi.com (loss=0%, rta=0.560000 ms)|loss=0%;;;0;100 rta=0.000560s;;;0.000000',
    'check_tcp': 'TCP OK - 0.092 second response time on port 3737',
    'check_memcached_hit': 'MEMCACHED OK - OK, Hit checked: OK - at 10.10.48.4:11211',
    'check_memcached_size': 'MEMCACHED OK - OK, Size checked: OK - at 10.10.245.10:11211',
    'check_mysql_health_connection_time': 'OK - 0.04 seconds to connect as usr_nagios',
    'check_mysql_health_slow_queries': 'OK - 0 slow queries in 1024 seconds (0.00/sec)',
    'check_mysql_health_slave-lag': 'Slave is 10 seconds behind master',
    'check_mysql_health_threads_connected': 'OK - 3 client connection threads',
    'check_mysql_health_slave-io-running': 'OK - Slave io is running',
    'check_mysql_health_slave-sql-running': 'OK - Slave sql is running',
    'check_memory':"Memory RAM OK - 9005560 kB free ( 17198668 kB used) | iso.3.6.1.4.1.2021.4.6.0=9005560 iso.3.6.1.4.1.2021.4.11.0=17198668",
    'check_passive': "cameras gcom/live:1 gnews/live:34 gsat/live1:0 gsat/live2:0 gsat/live3:0 g1rj1/live:0 g1sp1/live:89 bbb/pgma:569 bbb/pgmb:478 bbb/cam1:2 bbb/cam2:10 bbb/cam3:5 bbb/cam4:8 bbb/cam5:19 chat/dwt:0 chat/pjc:3 chat/ber1:1 chat/ber2:0 chat/cgj:0",
    'check_mysql_health_slave': "CRITICAL - cannot connect to information_schema. Can't connect to MySQL server on '10.10.138.49' (111)"
}

fakenagios.main(test_service)
