import fakenagios

test_service = {
    'check_cpu': 'CPU usage (%user %system %idle) OK - 0 0 99',
	'check_disk': 'Disk space OK - 64031408 kB free ( 3 % used) | iso.3.6.1.4.1.2021.9.1.7.1=64031408 iso.3.6.1.4.1.2021.9.1.9.1=3',
}

fakenagios.main(test_service)
