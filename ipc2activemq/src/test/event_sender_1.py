import fakenagios


apache_bws_off = {
    {'host': 'dvel-lav-01', 'eventtype': 'TCP', 'description': 'TCP OK - 0.01 second response time on port 80'},
    {'host': 'dvel-lav-01', 'eventtype': 'TCP', 'description': 'TCP CRITICAL - 0.01 second response time on port 80'},
    {'host': 'dvel-lav-01', 'eventtype': 'TCP', 'description': 'TCP CRITICAL - 0.01 second response time on port 80'},
    {'host': 'dvel-lav-01', 'eventtype': 'TCP', 'description': 'TCP CRITICAL - 0.01 second response time on port 80'},
}
apache_bws_on = {
    {'host': 'dvel-lav-01', 'eventtype': 'TCP', 'description': 'TCP CRITICAL - 0.01 second response time on port 80'},
    {'host': 'dvel-lav-01', 'eventtype': 'TCP', 'description': 'TCP CRITICAL - 0.01 second response time on port 80'},
    {'host': 'dvel-lav-01', 'eventtype': 'TCP', 'description': 'TCP CRITICAL - 0.01 second response time on port 80'},
    {'host': 'dvel-lav-01', 'eventtype': 'TCP', 'description': 'TCP OK - 0.01 second response time on port 80'},
}


disk_bws_error = {
    {'host': 'loma-ldr-01', 'eventtype': 'Disk', 'description': 'DISK CRITICAL - free space: /test 99 MB (6% inode=10%)'},
    {'host': 'loma-ldr-01', 'eventtype': 'Disk', 'description': 'DISK CRITICAL - free space: /test 99 MB (5% inode=10%)'},
    {'host': 'loma-ldr-01', 'eventtype': 'Disk', 'description': 'DISK CRITICAL - free space: /test 99 MB (4% inode=10%)'},
    {'host': 'loma-ldr-01', 'eventtype': 'Disk', 'description': 'DISK CRITICAL - free space: /test 99 MB (3% inode=10%)'},
}
disk_bws_warning = {
    {'host': 'loma-ldr-01', 'eventtype': 'Disk', 'description': 'DISK CRITICAL - free space: /test 99 MB (21% inode=10%)'},
    {'host': 'loma-ldr-01', 'eventtype': 'Disk', 'description': 'DISK CRITICAL - free space: /test 99 MB (10% inode=10%)'},
    {'host': 'loma-ldr-01', 'eventtype': 'Disk', 'description': 'DISK CRITICAL - free space: /test 99 MB (9% inode=10%)'},
    {'host': 'loma-ldr-01', 'eventtype': 'Disk', 'description': 'DISK CRITICAL - free space: /test 99 MB (11% inode=10%)'},
}
disk_bws_ok = {
    {'host': 'loma-ldr-01', 'eventtype': 'Disk', 'description': 'DISK CRITICAL - free space: /test 99 MB (3% inode=10%)'},
    {'host': 'loma-ldr-01', 'eventtype': 'Disk', 'description': 'DISK CRITICAL - free space: /test 99 MB (4% inode=10%)'},
    {'host': 'loma-ldr-01', 'eventtype': 'Disk', 'description': 'DISK CRITICAL - free space: /test 99 MB (5% inode=10%)'},
    {'host': 'loma-ldr-01', 'eventtype': 'Disk', 'description': 'DISK CRITICAL - free space: /test 99 MB (6% inode=10%)'},
}

host_bws_off = {
    {'host': 'dvel-lav-01', 'eventtype': 'Ping', 'description': 'PING OK - Packet loss = 0%, RTA = 25.0 ms'},
    {'host': 'dvel-lav-01', 'eventtype': 'Ping', 'description': 'PING CRITICAL - Packet loss = 100%, RTA = 2500.0 ms'},
    {'host': 'dvel-lav-01', 'eventtype': 'Ping', 'description': 'PING CRITICAL - Packet loss = 100%, RTA = 2500.0 ms'},
    {'host': 'dvel-lav-01', 'eventtype': 'Ping', 'description': 'PING CRITICAL - Packet loss = 100%, RTA = 2500.0 ms'},
}
host_bws_on = {
    {'host': 'dvel-lav-01', 'eventtype': 'Ping', 'description': 'PING CRITICAL - Packet loss = 100%, RTA = 2500.0 ms'},
    {'host': 'dvel-lav-01', 'eventtype': 'Ping', 'description': 'PING CRITICAL - Packet loss = 100%, RTA = 2500.0 ms'},
    {'host': 'dvel-lav-01', 'eventtype': 'Ping', 'description': 'PING CRITICAL - Packet loss = 100%, RTA = 2500.0 ms'},
    {'host': 'dvel-lav-01', 'eventtype': 'Ping', 'description': 'PING OK - Packet loss = 0%, RTA = 25.0 ms'},
}

test_service = {'diskOk' : 'Disk space OK - 8899052 kB free ( 39 % used)',
        'diskWarning' : 'Disk space WARNING - 6647236 kB free ( *61* % used)',
        'diskCritical' : 'Disk space CRITICAL - 6647224 kB free ( *61* % used)',
        'cpuOk' : 'CPU usage (%user %system %idle) OK - 0 0 99',
        'cpuWarning' : 'CPU usage (%user %system %idle) WARNING - 0 0 *99*',
        'cpuCritical' : 'CPU usage (%user %system %idle) CRITICAL - 0 0 *99*',
        'loadOk' : 'Load average OK - 0 0 0',
        'loadWarning' : 'Load average WARNING - 0 0 *2*',
        'loadCritical' : 'Load average CRITICAL - 0 0 *5*',
        'memoryOk' : 'Memory RAM OK - 81808 kB free ( 2088564 kB used)',
        'memoryWarning' : 'Memory RAM WARNING - *185900* kB free ( 2182264 kB used)',
        'memoryCritical' : 'Memory RAM CRITICAL - *185060* kB free ( 2181424 kB used)',
        'swapOk' : 'Swap OK - 2097144 kB total size ( 2097144 kB available space)',
        'swapWarning' : 'Swap WARNING - 2104504 kB total size ( *1996364* kB available space)',
        'swapCritical' : 'Swap CRITICAL - 2104504 kB total size ( *1996364* kB available space)',
        'queryOk' :"QUERY OK: 'select count(*) from nagios_hosts' returned 53.000000",
        'queryWarning' : "QUERY WARNING: 'select count(*) from nagios_hosts' returned 53.000000",
        'queryCritical' : "QUERY CRITICAL: 'select count(*) from nagios_hosts' returned 53.000000",
        'smtpOk' : 'SMTP OK - 0.010 sec. response time',
        'smtpWarning' : 'SMTP WARNING - 0.016 sec. response time',
        'smtpCritical' : 'SMTP CRITICAL - 0.550 sec. response time',        
        'srvvld48Ok' : 'FPING OK - srvvld48.test.com (loss=0%, rta=1.010000 ms)',
        'srvvld48Warning' : 'FPING WARNING - srvvld48.globoi.com (loss=0%, rta=0.560000 ms)',
        'srvvld48Critical' : 'FPING CRITICAL - srvvld48.test.com (loss=100% )'   
}

fakenagios.main(test_service)
