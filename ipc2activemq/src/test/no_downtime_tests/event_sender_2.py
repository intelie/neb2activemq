import fakenagios

test_service = {
    'check_http': [
        'HTTP OK HTTP/1.1 200 OK - 0.001 second response time |time=0.001378s;;;0.000000 size=259B;;;0',
        'HTTP OK - HTTP/1.1 301 Moved Permanently - 0.002 second response time',
        'HTTP OK - HTTP/1.1 302 Moved Temporarily - 0.000 second response time',
        'HTTP OK - HTTP/1.1 302 Object moved - 0.009 second response time',
        'HTTP WARNING: HTTP/1.1 400 Bad Request',
        'HTTP WARNING: HTTP/1.1 403 Forbidden',
        'HTTP WARNING: HTTP/1.1 404 Not Found',
        'HTTP WARNING: HTTP/1.1 404 NOT FOUND',
        'HTTP WARNING: HTTP/1.1 404 Object Not Found',
        'HTTP CRITICAL - string not found|time=0.001627s;;;0.000000 size=259B;;;0',
        'HTTP CRITICAL: HTTP/1.1 500 Internal Server Error',
        'HTTP CRITICAL: HTTP/1.1 500 INTERNAL SERVER ERROR',
        'HTTP CRITICAL: HTTP/1.1 500 Server Error',
        'HTTP CRITICAL: HTTP/1.1 502 Proxy Error',
        'HTTP CRITICAL: HTTP/1.1 503 Service Temporarily Unavailable',
        'HTTP CRITICAL: HTTP/1.1 503 Service Unavailable',
        'CRITICAL - Socket timeout after 5 seconds',
        'sbrubles\0'
    ],
    'check_cpu': [
        'CPU usage (%user %system %idle) OK - 0 0 99 | iso.3.6.1.4.1.2021.11.9.0=0 iso.3.6.1.4.1.2021.11.10.0=0 iso.3.6.1.4.1.2021.11.11.0=99',
        'CPU usage (%user %system %idle) WARNING - 0 0 *99* | iso.3.6.1.4.1.2021.11.9.0=0 iso.3.6.1.4.1.2021.11.10.0=0 iso.3.6.1.4.1.2021.11.11.0=99',
        'CPU usage (%user %system %idle) CRITICAL - 0 0 *99* | iso.3.6.1.4.1.2021.11.9.0=0 iso.3.6.1.4.1.2021.11.10.0=0 iso.3.6.1.4.1.2021.11.11.0=99'
    ],
    'check_disk': [
        'Disk space OK - 64031408 kB free ( 3 % used) | iso.3.6.1.4.1.2021.9.1.7.1=64031408 iso.3.6.1.4.1.2021.9.1.9.1=3',
        'Disk space WARNING - 64031408 kB free ( *3* % used) | iso.3.6.1.4.1.2021.9.1.7.1=64031408 iso.3.6.1.4.1.2021.9.1.9.1=3',
        'Disk space CRITICAL - 64031408 kB free ( *3* % used) | iso.3.6.1.4.1.2021.9.1.7.1=64031408 iso.3.6.1.4.1.2021.9.1.9.1=3'
    ],
    'check_load': [
        'Load average OK - 0 0 0 | iso.3.6.1.4.1.2021.10.1.3.1=0 iso.3.6.1.4.1.2021.10.1.3.2=0 iso.3.6.1.4.1.2021.10.1.3.3=0',
        'Load average WARNING - *1* 0 1 | iso.3.6.1.4.1.2021.10.1.3.1=1 iso.3.6.1.4.1.2021.10.1.3.2=0 iso.3.6.1.4.1.2021.10.1.3.3=1',
        'Load average CRITICAL - *1* 0 1 | iso.3.6.1.4.1.2021.10.1.3.1=1 iso.3.6.1.4.1.2021.10.1.3.2=0 iso.3.6.1.4.1.2021.10.1.3.3=1'
    ],
    'check_swap': [
        'Swap OK - 16780208 kB total size ( 16780112 kB available space) | iso.3.6.1.4.1.2021.4.3.0=16780208 iso.3.6.1.4.1.2021.4.4.0=16780112',
        'Swap WARNING - 16780208 kB total size ( *16780112* kB available space) | iso.3.6.1.4.1.2021.4.3.0=16780208 iso.3.6.1.4.1.2021.4.4.0=16780112',
        'Swap CRITICAL - 16780208 kB total size ( *16780112* kB available space) | iso.3.6.1.4.1.2021.4.3.0=16780208 iso.3.6.1.4.1.2021.4.4.0=16780112'
    ],
    'check_memcached_hit': [
        'MEMCACHED OK - OK, Hit checked: OK - at 10.10.48.4:11211',
        'MEMCACHED WARNING - Hit checked: NG - at 10.10.245.9:11211 | hits=83.67[%];@6:90;@6',
        'MEMCACHED CRITICAL - Hit checked: NG - at 10.10.245.9:11211 | hits=83.67[%];@85:90;@85',
        'MEMCACHED CRITICAL - Cant connect to 10.10.237.53'
    ],
    'check_memcached_size': [
        'MEMCACHED OK - OK, Size checked: OK - at 10.10.245.10:11211',
        'MEMCACHED WARNING - Size checked: NG - at 10.10.245.9:11211 | size=7.64[%];6;80',
        'MEMCACHED CRITICAL - Size checked: NG - at 10.10.245.9:11211 | size=7.64[%];5;6',
        'MEMCACHED CRITICAL - Can\'t connect to 10.10.245.12'
    ],
    'check_fping': [
        'FPING OK - riosf109.globoi.com (loss=0%, rta=0.560000 ms)|loss=0%;;;0;100 rta=0.000560s;;;0.000000',
        'FPING CRITICAL - riolf95.globoi.com (loss=100% )|loss=100%;;;0;100'
    ],
    'check_tcp': [
        'TCP OK - 0.092 second response time on port 3737',
        'TCP OK - 0.007 second response time on port 80|time=0.007330s;;;0.000000;10.000000',
        'CRITICAL - Socket timeout after 10 seconds',
        'TCP CRITICAL - Invalid hostname, address or socket: puppet02.globoi.com'
    ]
}
# TODO: missing MySQL checks

fakenagios.main(test_service)
