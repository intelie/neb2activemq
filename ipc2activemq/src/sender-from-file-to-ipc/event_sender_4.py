import fakenagios2

test_service = {
    'check_cpu': 'usage (%user %system %idle) OK - 0 0 99'
}

fakenagios2.main(test_service)
