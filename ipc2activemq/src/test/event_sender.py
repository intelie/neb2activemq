import fakenagios

test_service = {
	'check_downtime' : "Localhost is currently in scheduled downtime"
}

fakenagios.main(test_service)
