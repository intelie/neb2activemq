#Defines topics of interests to log from nagios and their regexps

# Do we need these error regexps?
errorRegexps = [
  {'properties': ['state'],
   'eventtype': 'MysqlCannotConnect',
   'regexp': r"(OK|WARNING|CRITICAL) - cannot connect to information_schema"
  },
  {'properties': ['state'],
   'eventtype': 'MysqlCannotConnect',
   'regexp': r"(OK|WARNING|CRITICAL) - connection could not be established"
  },
  {'properties': ['state'],
   'eventtype': 'MysqlCannotConnect',
   'regexp': r"(OK|WARNING|CRITICAL) - Socket timeout"
  },
]

expressions = {
    'check_tcp': [
        {'labelFilter': 'TCP',
         'eventtype': 'TCP',
         'regexps': [
            {'properties': ['state', 'response_time', 'port'],
             'regexp': r"TCP (OK|WARNING|CRITICAL) - ([\d.]+) seconds? response time on port (\d+)"
            },
            {'properties': ['state'],
             'regexp': r"TCP (OK|WARNING|CRITICAL) - Invalid"
            }
         ]
        },
        {'labelFilter': None,
         'eventtype': 'TCP',
         'regexps': [
            {'properties': ['state'],
             'regexp': r"(WARNING|CRITICAL) - Socket timeout"
            }
         ]
        }
    ],

    'check_load': [
        {'labelFilter': None,
         'eventtype': 'Load',
         'regexps': [
            {'properties': ['state', 'min1', 'min5', 'min15'],
             'regexp': r"(OK|WARNING|CRITICAL) - load average: ([\d.]+), ([\d.]+), ([\d.]+)"
            }
         ]
        }
    ],

    'check_cpu': [
        {'labelFilter': 'CPU',
         'eventtype': 'CPU',
         'regexps': [
            {'properties': ['state', 'user' , 'system', 'idle'], # ordenated!
             'regexp': r"CPU usage \(%user %system %idle\) (OK|WARNING|CRITICAL) - (\d+) (\d+) \*?(\d+)\*?"
	    },
            {'properties': ['state', 'min1', 'min5', 'min15'],
             'regexp': r"(OK|WARNING|CRITICAL) - load average: ([\d.]+), ([\d.]+), ([\d.]+)"
            },
            {'properties': ['state', 'percentual', 'type'],
             'regexp': r"(OK|WARNING|CRITICAL) - CPU em (\d+)%, tipo: (.+)"
            },
         ]
        }
    ],

    'check_cpu_snmp': [
        {'labelFilter': None,
         'eventtype': 'CPU',
         'regexps': [
            {'properties': ['state', 'percentual', 'type'],
             'regexp': r"(OK|WARNING|CRITICAL) - CPU em (\d+)%, tipo: (.+)"
            },
         ]
        }
    ],


#    'conn': [ #conn = check_fping
#        {'labelFilter': 'FPING',
#         'eventtype': 'PING',
#         'regexps': [
#            {'properties': ['state', 'ip', 'loss', 'rta'],
#             'regexp': r"FPING (OK|WARNING|CRITICAL) - ([\d.]+) \(loss=(\d+)%(?:(?:, rta=([\d.]+) ms\))|\(\))"
#            }
#         ]
#        }
#    ],

    'check_ping': [
        {'labelFilter': 'PING',
         'eventtype': 'PING',
         'regexps': [
            {'properties': ['state', 'loss', 'rta'],
             'regexp': r"PING (OK|WARNING|CRITICAL) - Packet loss = ([\d.]+)%, RTA = ([\d.]+) ms"
            }
         ]
        }
    ],

    'dns': [
        {'labelFilter': 'DNS',
         'eventtype': 'DNS',
         'regexps': [
            {'properties': ['state', 'response_time', 'dns_record', 'ip'],
             'regexp': r'DNS (OK|WARNING|CRITICAL): ([\d.]+) seconds? response time. ([^ ]+) returns ([\d.]+)'
            }
         ]
        }
    ],

    'ftp': [
        {'labelFilter': 'FTP',
         'eventtype': 'FTP',
         'regexps': [
            {'properties': ['state', 'response_time', 'port'],
             'regexp': r'FTP (OK|WARNING|CRITICAL) - ([\d.]+) seconds? response time on port ([\d]+)'
            },
         ]

        }
    ],

    'check_procs': [
        {'labelFilter': None,
         'eventtype': 'Procs',
         'regexps': [
            {'properties': ['state', 'number_of_processes', 'args'],
             'regexp': r'(OK|WARNING|CRITICAL) - ([\d]+) processes running with args (.+)'
            }
         ]

        }
    ],

    'check_local_procs': [
        {'labelFilter': None,
         'eventtype': 'Procs',
         'regexps': [
            {'properties': ['state', 'number_of_processes', 'state_of_process'],
             'regexp': r'PROCS (OK|WARNING|CRITICAL): ([\d]+) processes with STATE = (.+)'
            }
         ]
        }
    ],

    'check_many_procs': [
        {'labelFilter': None,
         'eventtype': 'ProcsNotRunning',
         'regexps': [
            {'properties': ['process_not_running'],
             'regexp': r'([^\(]+)'
            }
         ]
        }
    ],
    
    'http_args_follow': [
        {'labelFilter': None,
         'eventtype': 'HTTP',
         'regexps': [
            {'properties': ['url', 'state', 'http_version', 'status_code', 'status_description', 'bytes', 'response_time'],
             'regexp': r'<A HREF="([^"]+)" target="_blank">HTTP (.+): HTTP/([\d.]+) ([\d]+) (.+) - ([\d]+) bytes in ([\d.]+) second response time </A>'
            }
         ]
        },
        {'labelFilter': None,
         'eventtype': 'HTTP',
         'regexps': [
            {'properties': ['url', 'state', 'status_description'],
             'regexp': r'<A HREF="([^"]+)" target="_blank">HTTP (.+) - (.+)'
            }
         ]
        },
        {'labelFilter': None,
         'eventtype': 'HTTP',
         'regexps': [
            {'properties': ['url', 'status_description'],
             'regexp': r'<A HREF="([^"]+)" target="_blank">(Connection refused)'
            }
         ]
        },
    ],

    'check_disk': [
        {'labelFilter': 'Disk',
         'eventtype': 'Disk',
         'regexps': [
            {'properties': ['state', 'free_space' , 'usage'],
             'regexp': r"Disk space (OK|WARNING|CRITICAL) - (\d+) kB free \( \*?(\d+)\*? % used\)"
             #'regexp': r'Disk space (OK|WARNING|CRITICAL) - (\d+) kB free \( (\w+) % used\) .*'
            }
         ]
        }
    ],

    'check_http': [
        {'labelFilter': None,
         'eventtype': 'HTTP',
         'regexps': [
            {'properties': ['state', 'status' , 'bytes_returned', 'response_time'],
             'regexp': r'HTTP (OK|WARNING): HTTP\/1.1 (\d{3}) .* - (\d+) bytes in ([\d.]+).*'
            }
         ]
        },
	{'labelfilter': None,
	 'eventtype': 'HTTP',
	 'regexps' : [
	   {'properties': ['state'],
	    'regexp': r'(CRITICAL) - Socket timeout after 10 seconds'
	   }
	]
      }
    ],



    'check_drbd': [
        {'labelFilter': 'DRBD',
         'eventtype': 'DRBD',
         'regexps': [
            {'properties': ['status', 'order', 'connected', 'updated'],
             'regexp': r'DRBD ([^:]+): Device 0 ([^ ]+) ([^ ]+) ([^ ]+)'
            }
         ]
        }
    ],

    'check_local_swap': [
        {'labelFilter': 'SWAP',
         'eventtype': 'SWAP',
         'regexps': [
            {'properties': ['state', 'free_memory'],
             'regexp': r'SWAP (OK|WARNING|CRITICAL) - (\d+)% free .*'
            }
         ]
        }
    ],

    'check_local_users': [
        {'labelFilter': 'USERS',
         'eventtype': 'USERS',
         'regexps': [
            {'properties': ['state', 'users'],
             'regexp': r'USERS (OK|WARNING|CRITICAL) - (\d+) .*'
            }
         ]
        }
    ],

    'check_ssh': [
        {'labelFilter': 'SSH',
         'eventtype': 'SSH',
         'regexps': [
            {'properties': ['state'],
             'regexp': r'SSH (OK|WARNING|CRITICAL) .*'
            }
         ]
        }
    ],

    'check_smtp': [
        {'labelFilter': 'SMTP',
         'eventtype': 'SMTP',
         'regexps': [
            {'properties': ['state', 'response_time'],
             'regexp': r'SMTP (OK|WARNING|CRITICAL) - ([\d.]+) .*'
            }
         ]
        }
    ],


    'check_heartbeat': [
        {'labelFilter': None,
         'eventtype': 'HEARTBEAT',
         'regexps': [
            {'properties': ['status', 'mode'],
             'regexp': r'Heartbeat (OK|WARNING|CRITICAL) - Modo (.+)'
            }
         ]
        }
    ],

    'check_mysql': [
        {'labelFilter': None,
         'eventtype': 'MYSQL',
         'regexps': [
            {'properties': ['uptime', 'threads', 'questions', 'slow_queries', 'opens', 'flush_tables', 'open_tables', 'average_queries_per_second'],
             'regexp': r'Uptime: ([\d]+)  Threads: ([\d]+)  Questions: ([\d]+)  Slow queries: ([\d]+)  Opens: ([\d]+)  Flush tables: ([\d]+)  Open tables: ([\d]+)  Queries per second avg: ([\d.]+)'
            }
         ]
        }
    ],

}
    ### STOPPED HERE ###
'''

    'check_propel_pwas450': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_ldap_time54': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'http_regexp': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_fila_ldap': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_replica_ibest2': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_nrpe': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'https': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_local_disk': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_process_nossl': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_raid': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],
    'host': [
        {'labelFilter': None,
         'eventtype': 'PING',
         'regexps': [
            {'properties': ['state', 'ip', 'loss', 'rta'],
             'regexp': r'FPING (OK|WARNING|CRITICAL) - ([0-9.]+) \(loss=([0-9]+)%, rta=([0-9.]+) ms\)'
            },
            {'properties': ['state', 'ip', 'loss'],
             'regexp': r'FPING (OK|WARNING|CRITICAL) - ([0-9.]+) \(loss=([0-9]+)% \)'
            },
            {'properties': ['ip'],
             'regexp': 'CRITICAL - Host Unreachable \(([0-9.]+)\)'
            },
         ]
        }
    ],
}
    '''

expressions['tcp'] = expressions['check_tcp']

expressions['check_local_load'] = expressions['check_load']

expressions['http_args'] = expressions['http_args_follow']
expressions['https'] = expressions['http_args_follow']
expressions['https_args'] = expressions['http_args_follow']
expressions['http_regexp'] = expressions['http_args_follow']

expressions['check_local_disk'] = expressions['check_disk']
