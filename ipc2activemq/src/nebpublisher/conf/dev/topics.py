errorRegexps = [
  {
    'properties' : ['state'],
    'eventtype' : 'MysqlCannotConnect',
    'regexp' : r"(OK|WARNING|CRITICAL) - cannot connect to information_schema"
  },
  {
    'properties' : ['state'],
    'eventtype' : 'MysqlCannotConnect',
    'regexp' : r"(OK|WARNING|CRITICAL) - connection could not be established"
  },
  {
    'properties' : ['state'],
    'eventtype' : 'MysqlCannotConnect',
    'regexp' : r"(OK|WARNING|CRITICAL) - Socket timeout"
  }
]

expressions = {
      'check_cpu' : [
        {
        'labelFilter': 'CPU',
        'eventtype' : 'CPU',
        'regexps' : [{
                       'properties' : ['state', 'user' , 'system', 'idle'], # ordenado !
                       'regexp' : r"CPU usage \(%user %system %idle\) (OK|WARNING|CRITICAL) - (\d+) (\d+) \*?(\d+)\*?"
                    }]
        }
				],
			'check_disk' : [
				{
        'labelFilter': 'Disk',
        'eventtype' : 'Disk',
        'regexps' : [{
                     'properties' : ['state', 'free_space' , 'usage'],
                     'regexp' : r"Disk space (OK|WARNING|CRITICAL) - (\d+) kB free \( \*?(\d+)\*? % used\)"
                   }]
        }
				],
			'check_load' : [
				{
        'labelFilter': 'Load',
        'eventtype' : 'Load',
        'regexps' : [{
                     'properties' : ['state', '1min', '5min', '15min'],
                     'regexp' : r"Load average (OK|WARNING|CRITICAL) - \*?(\d+)\*? \*?(\d+)\*? \*?(\d+)\*?"
                   }]
        }
				],
			'check_swap' : [
				{
					'labelFilter': 'Swap',
	        'eventtype' : 'Swap',
	        'regexps' : [{
	                     'properties' : ['state', 'total', 'available'],
	                     'regexp' : r"Swap (OK|WARNING|CRITICAL) - \*?(\d+)\*? kB total size \( \*?(\d+)\*? kB available space\)"
	                   }]
	      }
				],
			'check_http' : [ 
	        {
	        'labelFilter': 'HTTP',
	        'eventtype' : 'HTTP',
	        'regexps' : [{
	                     'properties' : ['state', 'status_code', 'response_time'],
	                     'regexp' : r"HTTP (OK) -? ?HTTP/1\.1 (\d+) .+ - (\d+.\d+) seconds? response time"
	                   },
										{
											'properties' : ['state', 'status_code'],
	                     'regexp' : r"HTTP (WARNING|CRITICAL):? ?-? HTTP/1\.1 (\d+) "
										},
										{
											'properties' : ['state'],
											'regexp' : r"HTTP (CRITICAL) - string not found"
										},
										]
							},
							{
								'labelFilter' : None,
								'eventtype' : 'HTTP',
								'regexps' :  [{
									'properties' : ['state'],
									'regexp' : r"(CRITICAL) - Socket timeout after 5 seconds"
								}]
							}
	        ],
			'check_fping' : [
				{
				'labelFilter' : 'FPING',
				'eventtype' : 'FPING',
				'regexps' : [{
					'properties' : ['state', 'loss', 'rta'],
					'regexp' : r"FPING (OK|WARNING|CRITICAL) -.+\(loss=(\d+)%(?:(?:, rta=(\d+\.\d*) ms\))|())"
					}]
				}
			],
			'check_tcp' : [
					{
				 	'labelFilter' : 'TCP',
					'eventtype' : 'TCP',
					'regexps' : [{
						'properties' : ['state', 'response_time', 'port'],
						'regexp' : r"TCP (OK|WARNING|CRITICAL) - (\d+.\d+) second response time on port (\d+)"
					},
					{
						'properties' : ['state'],
						'regexp' : r"TCP (OK|WARNING|CRITICAL) - Invalid"
					}]
				},
				{
				 	'labelFilter' : None,
					'eventtype' : 'TCP',
					'regexps' : [{
						'properties' : ['state'],
						'regexp' : r"(WARNING|CRITICAL) - Socket timeout"
					}]
				}
			],
		  'check_memcached_hit' : [
			    {
           'labelFilter' : 'MEMCACHED',
           'eventtype' : 'MemCachedHit',
           'regexps' : [{
             'properties' : ['state', 'hits'],
             'regexp' : r"MEMCACHED (OK|WARNING|CRITICAL).+ hits=(\d+\.\d+)"
             }]
           },
           {
            'labelFilter' : 'MEMCACHED',
            'eventtype' : 'MemCachedHit',
            'regexps' : [{
              'properties' : ['state'],
              'regexp' : r"MEMCACHED (OK|WARNING|CRITICAL) -"
              }]
            }
       ],
      'check_memcached_size' : [
		    {
        'labelFilter' : 'MEMCACHED',
        'eventtype' : 'MemCachedSize',
        'regexps' : [{
          'properties' : ['state', 'size'],
          'regexp' : r"MEMCACHED (OK|WARNING|CRITICAL).+ size=(\d+\.\d+)"
          }]
        },
        {
         'labelFilter' : 'MEMCACHED',
         'eventtype' : 'MemCachedSize',
         'regexps' : [{
           'properties' : ['state'],
           'regexp' : r"MEMCACHED (OK|WARNING|CRITICAL) -"
           }]
         }
       ],
       'check_mysql_health_connection_time': [
          {
           'labelFilter' : None,
           'eventtype' : 'MysqlHealthConnectionTime',
           'regexps' : [{
             'properties' : ['state', 'seconds', 'user'],
             'regexp' : r"(OK|WARNING|CRITICAL) - (\d+\.\d+) seconds to connect as (\S+)"
             }]
           }
       ],
       'check_mysql_health_slow_queries' : [
        {
         'labelFilter' : None,
         'eventtype' : 'MysqlHealthSlowQueries',
         'regexps' : [{
           'properties' : ['state', 'count', 'window'],
           'regexp' : r"(OK|WARNING|CRITICAL) - (\d+) slow queries in (\d+) seconds"
           }]
         }
       ],
       'check_mysql_health_slave-lag' : [
          {
           'labelFilter' : None,
           'eventtype' : 'MysqlHealthSlaveLag',
           'regexps' : [{
             'properties' : ['state', 'seconds'],
             'regexp' : r"(OK|WARNING|CRITICAL) - Slave is (\d+) seconds behind master"
             }]
           }
       ],
       'check_mysql_health_threads_connected' : [
          {
           'labelFilter' : None,
           'eventtype' : 'MysqlHealthThreadsConnected',
           'regexps' : [{
             'properties' : ['state', 'count'],
             'regexp' : r"(OK|WARNING|CRITICAL) - (\d+) client connection threads"
             }]
           }
       ], 
       'check_mysql_health_slave-io-running' : [
          {
           'labelFilter' : None,
           'eventtype' : 'MysqlHealthSlaveIORunning',
           'regexps' : [{
             'properties' : ['state'],
             'regexp' : r"(OK|WARNING|CRITICAL) - Slave io"
             }]
           }
       ],
       'check_mysql_health_slave-sql-running' : [
           {
            'labelFilter' : None,
            'eventtype' : 'MysqlHealthSlaveSqlRunning',
            'regexps' : [{
              'properties' : ['state'],
              'regexp' : r"(OK|WARNING|CRITICAL) - Slave sql"
              }]
            }
        ]
}
