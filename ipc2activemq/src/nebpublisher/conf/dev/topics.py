# -*- coding: utf-8 -*-
import copy

expressions = {
# new
    'check_bond': [
        {'eventtype': 'Bond',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state'],
             'regexp': r'(OK|WARNING|CRITICAL):.*'
            }
         ]
        }
    ],


    'check_crm': [
        {'eventtype': 'Crm',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state', 'time'],
             'regexp': r'WebInject (OK|WARNING|CRITICAL) - All tests passed successfully in ([0-9.]+) seconds$'
            },
            {'properties': [],
             'regexp': r'\(No output returned from plugin\)'
            }
         ]
        }
    ],


    'check_current_componentes': [
        {'eventtype': 'CurrentComponentes',
         'labelFilter': None,
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
     ],


    'check_current_templates': [
        {'eventtype': 'CurrentTemplates',
         'labelFilter': None,
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],


    'check_dig': [
        {'eventtype': 'Dig',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state', 'response_time', 'host', 'status', 'ip'],
             'regexp': r'DNS (OK|WARNING|CRITICAL) - ([0-9.]+) seconds? response time \((.*) ([0-9]+) IN A (.*)\)'
            }
         ]
        }
    ],

    'check_uptime': [
        {'eventtype': 'Uptime',
         'labelFilter': None,
         'regexps': [
            {'properties': ['day', 'hour', 'minute'],
             'regexp': r'System Uptime - (\d+) day\(s\) (\d+) hour\(s\) (\d+) minute\(s\)'
            },
         ]
        }
    ],

    'check_dns_recursive': [
        {'eventtype': 'DNSRecursive',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state'],
             'regexp': r'\w+ (OK|WARNING|CRITICAL)'
            }
         ]
        }
    ],


 'check_dummy': [
     {'eventtype': 'Type',
                  'labelFilter': None,
                  'regexps': [{'properties': ['state', 'response_time', 'port'],
                               'regexp': r'TCP (OK|WARNING|CRITICAL) - ([\d.]+) seconds* response time on port (\d+)'
            		      },
			      {'properties': ['state', 'loss', 'rta'],
			       'regexp': r'PING (OK|WARNING|CRITICAL) - Packet loss = (\d+)%, RTA = ([\d.]+) ms'
			      },
			      {'properties': ['state', 'status', 'bytes_returned', 'response_time'],
			       'regexp': r'HTTP (OK|WARNING|CRITICAL) HTTP\/1.1 (\d+) OK - (\d+) bytes in ([\d.]+) seconds*'
			      },
			      {'properties': ['state', 'response_time', 'port'],
			       'regexp': r'FTP (OK|WARNING|CRITICAL) - ([\d.]+) seconds* response time on port (\d+) .+'
			      },
			      {'properties': ['state', 'path','free_space','percentage_free_space', 'free_inode_percentage'],
			       'regexp': r'DISK (OK|WARNING|CRITICAL) - free space: (.+) (\d+) MB \((\d+)% inode=(\d+)%\)'
			      },
			      {'properties': ['state', 'packages_to_upgrade', 'critical_updates'],
			       'regexp': r'APT (OK|WARNING|CRITICAL): (\d+) packages available for upgrade \((\d+) critical updates\)'
			      },
			      {'properties': ['state', 'output'],
			       'regexp': r'(OK|WARNING|CRITICAL): (.+)'
			      },
			      {'properties': ['state', 'processes'],
			       'regexp': r'PROCS (OK|WARNING|CRITICAL): (\d+) processes'
			      },
			      {'properties': ['state', 'processes_state_Z'],
			       'regexp': r'PROCS (OK|WARNING|CRITICAL): (\d+) processes with STATE = Z'
			      },
			      {'properties': ['uptime', 'threads', 'questions', 'slow_queries', 'opens', 'flush_tables', 'open_tables', 'queries_second'],
			       'regexp': r'Uptime: (\d+)  Threads: (\d+)  Questions: (\d+)  Slow queries: (\d+)  Opens: (\d+)  Flush tables: (\d+)  Open tables: (\d+)  Queries per second avg: ([\d.]+)'
			      },
			      {'properties': ['state'],
			       'regexp': r'AUTH (OK|WARNING|CRITICAL)'
			      },
			      {'properties': ['service', '', 'timestamp'],
			       'regexp': r'(.+):(\d+) expires on (.+)'
			      }
         ]
        }
    ],


    'check_elasticsearch': [
        {'eventtype': 'ElasticSearch',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state', 'version', 'status_code', 'status_description', 'bytes', 'response_time'],
             'regexp': r'HTTP (OK|WARNING|CRITICAL): HTTP/([0-9.]+) ([0-9]{3}) (.+) - ([0-9]+) bytes in ([0-9.]+) second response time'
            }
         ]
        }
    ],


    'check_elasticsearch_alias': [
        {'eventtype': 'ElasticSearchAlias',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state', 'version', 'status_code', 'status_description', 'bytes', 'response_time'],
             'regexp': r'HTTP (OK|WARNING|CRITICAL): HTTP/([0-9.]+) ([0-9]{3}) (.+) - ([0-9]+) bytes in ([0-9.]+) second response time'
            }
         ]
        }
    ],


    'check_enquete': [
        {'eventtype': 'Enquete',
         'labelFilter': None,
         'regexps': [{'properties': ['state'],
                     'regexp': r'(OK|WARNING|CRITICAL):.*'
            }
         ]
        }
    ],


    'check_firewall_rules': [
        {'eventtype': 'FirewallRules',
         'labelFilter': None,
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],


    'check_ftp_args': [
        {'eventtype': 'FTP',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state', 'response_time', 'port'],
             'regexp': r'FTP (OK|WARNING|CRITICAL) - ([0-9.]+) \w+ response time on port ([0-9]+) .*'
            }
         ]
        }
    ],


    'check_hash': [
        {'eventtype': 'Hash',
         'labelFilter': None,
         'regexps': [
            {'properties': ['hash'],
             'regexp': r'([0-9]+)'
            }
         ]
        }
    ],

    'check_jvm_wrapper': [
        {'eventtype': 'JVMWrapper',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state', 'thread_blocked', 'waiti', 'timed_waiting', 'classes', 'pe_ding', 'heap_used', 'nonheap_used', 'code_used', 'eden_used', 'survivor_used', 'oldgen_used', 'permgen_used'],
             'regexp': r'(OK|WARNING|CRITICAL): threads=blocked:([0-9]+) waiti\/g:([0-9]+) timedWaiting:([0-9]+), objects=classes:([0-9]+) pe\/ding:([0-9]+), heap=used:([0-9]+)%, nonheap=used:([0-9]+)%, code=used:([0-9]+)%, eden=used:([0-9]+)%, survivor=used:([0-9]+)%, oldgen=used:([0-9]+)%, permgen=used:([0-9]+)%'
            }
         ]
        }
    ],


    'check_ldap': [
        {'eventtype': 'Ldap',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state', 'response_time'],
             'regexp': r'LDAP (OK|WARNING|CRITICAL) - ([0-9.]+) \w+ response time'
            }
         ]
        }
    ],


    'check_ldap_mail': [
        {'eventtype': 'LdapMail',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state', 'response_time'],
             'regexp': r'LDAP (OK|WARNING|CRITICAL) - ([0-9.]+) \w+ response time'
            }
         ]
        }
    ],


    'check_ldap_mail_bsb': [
        {'eventtype': 'LdapMailBsb',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state', 'response_time'],
             'regexp': r'LDAP (OK|WARNING|CRITICAL) - ([0-9.]+) \w+ response time'
            }
         ]
        }
    ],


    'check_ldap_time': [
        {'eventtype': 'LdapTime',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state', 'host_name', 'timestamp'],
             'regexp': r'(OK|WARNING|CRITICAL) - Timestemp (\S+) (.+)'
            }
         ]
        }
    ],


    'check_memcached': [
        {'eventtype': 'LdapMemcached',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state', 'accepting_conns', 'bytes', 'bytes_read', 'bytes_written', 'conn_yields', 'connection_structures', 'curr_connections', 'curr_items'],
             'regexp': r'(OK|WARNING|CRITICAL): accepting_conns: ([0-9]+), bytes: ([0-9]+), bytes_read: ([0-9]+), bytes_written: ([0-9]+), conn_yields: ([0-9]+), connection_structures: ([0-9]+), curr_connections: ([0-9]+), curr_items: ([0-9]+)'
            }
         ]
        }
    ],


    'check_mms': [
        {'eventtype': 'Mms',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state'],
             'regexp': r'(OK|WARNING|CRITICAL) - .*'
            }
         ]
        }
    ],


    'check_mule': [
        {'eventtype': 'Mule',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state'],
             'regexp': r'(OK|WARNING|CRITICAL):.*'
            }
         ]
        }
    ],


    'check_nrpe_args': [
        {'eventtype': 'NrpeArgs',
         'labelFilter': None,
         'regexps': [
            {'properties': ['url', 'state', 'version', 'status_code', 'status_description', 'bytes', 'response_time'],
             'regexp': r'<A HREF="(.+)" target="_blank">HTTP (OK|WARNING|CRITICAL): HTTP\/([0-9.]+) ([0-9]{3}) (.+) - ([0-9]+) bytes in ([0-9.]+) second response time <\/A>'
            },
            {'properties': ['state', 'version', 'status_code', 'status_description', 'bytes', 'response_time'],
             'regexp': r'HTTP (OK|WARNING|CRITICAL): HTTP/([0-9.]+) ([0-9]{3}) (.+) - ([0-9]+) bytes in ([0-9.]+) second response time'
            },
            {'properties': ['state', 'queue'],
             'regexp': r'(OK|WARNING|CRITICAL) - Fila: ([0-9]+)'
            }
         ]
        }
    ],

    'check_snmp_procs': [
        {'eventtype': 'SNMP',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state', 'collectord', 'opt'],
             'regexp': r'(OK|WARNING|CRITICAL): \.\/(.+) \-\-(.+)'
            },
            {'properties': ['state', 'file_1'],
             'regexp': r'(OK|WARNING|CRITICAL): ([^, ]+)+'
            }
         ]
        }
    ],



    'check_nrpe_cmd': [
        {'eventtype': 'Type',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state', 'file', 'age', 'bytes'],
             'regexp': 'FILE_AGE (OK|WARNING|CRITICAL): (.*) is ([0-9]+) seconds? old and ([0-9]+) bytes'
            }
         ]
        }
    ],


    'check_ntp_time': [
        {'eventtype': 'NrpeTime',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state', 'time'],
             'regexp': r'NTP (OK|WARNING|CRITICAL): Offset (-?[0-9.]+) secs'
            }
         ]
        }
    ],


    'check_pop': [
        {'eventtype': 'Pop',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state', 'response_time', 'port'],
             'regexp': r'POP (OK|WARNING|CRITICAL) - ([0-9.]+) second response time on port ([0-9]+).*'
            }
         ]
        }
    ],


    'check_postfix_queue': [
        {'eventtype': 'PostfixQueue',
         'labelFilter': None,
         'regexps': [
            {'properties': ['messages'],
             'regexp': r'Number of queued messages: ([0-9]+)'
            }
         ]
        }
    ],


    'check_propel_7797': [
        {'eventtype': 'Propel7797',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state'],
             'regexp': r'.*(OK|WARNING|CRITICAL)\.$'
            }
         ]
        }
    ],


    'check_propel_7798': [
        {'eventtype': 'Propel7798',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state'],
             'regexp': r'.*(OK|WARNING|CRITICAL)\.$'
            }
         ]
        }
    ],


    'check_propel_conns': [
        {'eventtype': 'PropelConns',
         'labelFilter': None,
         'regexps': [
            {'properties': ['active_conns'],
             'regexp': r'Active Connections: ([0-9]+)'
            }
         ]
        }
    ],


    'check_propel_pwas450': [
        {'eventtype': 'Type',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state'],
             'regexp': '.*status: (OK|WARNING|CRITICAL)'
            }
         ]
        }
    ],


    'check_radiusconnect': [
        {'eventtype': 'RadiusConnect',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state', 'code'],
             'regexp': r'Radius-Request (OK|WARNING|CRITICAL) -\[.*\] code: ([0-9]+)'
            }
         ]
        }
    ],


    'check_sftp': [
        {'eventtype': 'SFTP',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state'],
             'regexp': r'Servico (OK|WARNING|CRITICAL)'
            }
         ]
        }
    ],


    'check_smtp': [
        {'eventtype': 'SMTP',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state', 'response_time'],
             'regexp': r'SMTP (OK|WARNING|CRITICAL) - ([0-9.]+) sec. response time'
            },
         ]
        }
    ],


      'check_snmp': [
     {'eventtype': 'Type',
                 'labelFilter': None,
                 'regexps': [{'properties': ['state', 'virtual_memory_used'],
                              'regexp': 'SNMP (OK|WARNING|CRITICAL) - (\d+) Virtual Memory Used'
            		     },
                             {'properties': ['state', 'physical_memory_used'],
                              'regexp': 'SNMP (OK|WARNING|CRITICAL) - (\d+) Physical Memory Used'
            		     },
                             {'properties': ['state', 'total_memory'],
                              'regexp': 'SNMP (OK|WARNING|CRITICAL) - (\d+) Total Memory'
            		     },
                             {'properties': ['state', 'system_status'],
                              'regexp': 'SNMP (OK|WARNING|CRITICAL) - "The system\'s global status is (\w+). "'
            		     },
                             {'properties': ['state', 'timeticks', 'days', 'time'],
                              'regexp': 'SNMP (OK|WARNING|CRITICAL) - Timeticks: \((\d+)\) (\d+) days, (.+)'
            		     }
                             
         ]
        }
    ],


 'check_snmp_load': [
     {'eventtype': 'Type',
                      'labelFilter': None,
                      'regexps': [{'properties': ['min1', 'min5', 'min15', 'state'],
                                   'regexp': 'Load : ([0-9.]+) ([0-9.]+) ([0-9.]+) : (OK|WARNING|CRITICAL)'
            }
         ]
        }
    ],


    'check_snmp_mem': [
        {'eventtype': 'SNMPMem',
         'labelFilter': None,
         'regexps': [
            {'properties': ['ram', 'swap', 'state'],
             'regexp': r'Ram : ([0-9]+)%, Swap : ([0-9]+)% : : (OK|WARNING|CRITICAL)'
            }
         ]
        }
    ],


 'check_snmp_procs_oas': [
     {'eventtype': 'Type',
                           'labelFilter': None,
                           'regexps': [{'properties': ['state', 'file_1', 'file_2'],
                                        'regexp': '(OK|WARNING|CRITICAL): (\S+) (\S+)'
            			       },
				       {'properties':[],
					'regexp': ''
				       }
         			      ]
        }
    ],


    'check_snmp_time': [
        {'eventtype': 'SNMPTime',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state', 'date', 'time'],
             'regexp': r'(OK|WARNING|CRITICAL): Data\/Hora = ([0-9/]+) ([0-9:]+)'
            }
         ]
        }
    ],


    'check_solr': [
        {'eventtype': 'Solr',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state'],
             'regexp': r'Solr (OK|WARNING|CRITICAL)'
            },
            {'properties': ['state','action','core','status'],
             'regexp': r'(OK|WARNING|CRITICAL): (.+) - core ([^ ]+) (OK)'
            }
         ]
        }
    ],


    'check_storage_snmp': [
        {'eventtype': 'Type',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state'],
             'regexp': '(OK|WARNING|CRITICAL)'
            },
			{'properties': ['state', 'file_1'],
			 'regexp': '(OK|WARNING|CRITICAL): ([^, ]+)+'
			}
         ]
        }
    ],


    'check_tcp_args': [
        {'eventtype': 'TCPArgs',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state', 'response_time', 'port'],
             'regexp': r'TCP (OK|WARNING|CRITICAL) - ([0-9.]+) second response time on port ([0-9]+)'
            }
         ]
        }
    ],


    'check_varnish': [
        {'eventtype': 'Varnish',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state', 'fetch_zero', 's_pass', 'backend_conn', 
                            'fetch_chunked', 'n_wrk_max', 'n_vampireobject', 
                            'n_vcl', 'esi_parse', 'esi_errors', 
                            'n_vcl_avail', 's_fetch', 'n_purge_dups', 
                            'sma_bfree', 'client_drop_late', 'shm_cycles', 
                            'n_deathrow', 'fetch_bad', 'backend_fail',
                            's_pipe', 'n_smf_large', 'n_purge', 
                            'backend_unhealthy', 'fetch_length'],
             'regexp': '(OK|WARNING|CRITICAL): fetch_zero: ([0-9]+), s_pass: ([0-9]+), backend_conn: ([0-9]+), fetch_chunked: ([0-9]+), n_wrk_max: ([0-9]+), n_vampireobject: ([0-9]+), n_vcl: ([0-9]+), esi_parse: ([0-9]+), esi_errors: ([0-9]+), n_vcl_avail: ([0-9]+), s_fetch: ([0-9]+), n_purge_dups: ([0-9]+), sma_bfree: ([0-9]+), client_drop_late: ([0-9]+), shm_cycles: ([0-9]+), n_deathrow: ([0-9]+), fetch_bad: ([0-9]+), backend_fail: ([0-9]+), s_pipe: ([0-9]+), n_smf_large: ([0-9]+), n_purge: ([0-9]+), backend_unhealthy: ([0-9]+), fetch_length: ([0-9]+).*'
            },
            {'properties': [],
             'regexp': '\(null\)'}
         ]
        }
    ],


    'check_vmware': [
        {'eventtype': 'VMWare',
         'labelFilter': None,
         'regexps': [
            {'properties': ['memory_usage'],
             'regexp': 'Memory usage at ([0-9.]+)%'
            },
            {'properties': ['cpu_usage'],
             'regexp': 'CPU usage at ([0-9.]+)%'
            },
            {'properties': ['network_usage'],
             'regexp': 'Network usage at ([0-9]+)Kbps'}
         ]
        }
    ],

    'check_webinject': [
        {'labelFilter': None,
         'eventtype': 'WebInject',
         'regexps': [
            {'properties': ['state', 'time'],
             'regexp': r'WebInject (OK|WARNING|CRITICAL) - All tests passed successfully in ([0-9.]+) seconds.*'
            },
            {'properties': ['state', 'timeout'],
             'regexp': r'WebInject (OK|WARNING|CRITICAL) - All tests passed successfully but global timeout \(([0-9]+) seconds\) has been reached'
            },
            {'properties': ['state', 'failed_test_num'],
             'regexp': r'WebInject (OK|WARNING|CRITICAL) - Test case number (\d+) failed'
            },
            {'properties': [],
             'regexp': r'No output returned from plugin'
            },
         ]
        }
    ],


    'check_webinject_oi': [
        {'eventtype': 'WebinjectOi',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state', 'time'],
             'regexp': r'WebInject (OK|WARNING|CRITICAL) - All tests passed successfully in ([0-9.]+) seconds.*'
            },
            {'properties': ['state', 'timeout'],
             'regexp': r'WebInject (OK|WARNING|CRITICAL) - All tests passed successfully but global timeout \(([0-9]+) seconds\) has been reached'
            }
         ]
        }
    ],


    'check_win_snmp_cpu': [
        {'eventtype': 'WinSNMPCpu',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state', 'load'],
             'regexp': r'(OK|WARNING|CRITICAL) : CPU Load ([0-9]+)%'
            }
         ]
        }
    ],


    'openfire-backend': [
        {'eventtype': 'OpenfireBackend',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state', 'status', 'bytes', 'response_time'],
             'regexp': 'HTTP (OK|WARNING|CRITICAL): .* ([0-9]{3}) \w+ - ([0-9]+) bytes in ([0-9.]+) \w+ response time'
            }
         ]
        }
    ],


    'webchat-status': [
        {'eventtype': 'WebchatStatus',
         'labelFilter': None,
         'regexps': [
            {'properties': ['state', 'status', 'bytes', 'response_time'],
             'regexp': 'HTTP (OK|WARNING|CRITICAL): .* ([0-9]{3}) \w+ - ([0-9]+) bytes in ([0-9.]+) \w+ response time'
            }
         ]
        }
    ],


# old
    'check_disk_NT': [
        {'labelFilter': None,
         'eventtype': 'Disk',
         'regexps': [
            {'properties': ['state', 'partition', 'free_percent'],
             'regexp': r'DISK (OK|WARNING|CRITICAL) - (.*) - Total: .* - Free: .* \((\d+)%\) - Used: .*'
            },
         ],
        },
    ],


    'check_mem': [
        {'labelFilter': None,
         'eventtype': 'Memory',
         'regexps': [
            {'properties': ['state', 'free_percent'],
             'regexp': r'Memory (OK|WARNING|CRITICAL) - ([0-9.]+)% .*'
            },
            {'properties': ['total', 'total_unit', 'used', 'used_unit', 'used_percentage', 'free', 'free_unit', 'free_percentage'],
             'regexp': r'Memory usage: total:([0-9.]+) (\w{2}) - used: ([0-9.]+) (\w{2}) \(([0-9]+)%\) - free: ([0-9.]+) (\w{2}) \(([0-9]+)%\)'
            },
         ],
        },
    ],


    'check_ram': [
        {'labelFilter': None,
         'eventtype': 'Memory',
         'regexps': [
            {'properties': ['state', 'free_total'],
             'regexp': r'RAM (OK|WARNING|CRITICAL) - Physical memory is.* \((\d+) MB\)'
            },
         ],
        },
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


    'check_swap': [
        {'labelFilter': None,
         'eventtype': 'Swap',
         'regexps': [
            {'properties': ['state', 'free_percent'],
             'regexp': r'SWAP (OK|WARNING|CRITICAL) - ([0-9]+)% free.*'
            },
            {'properties': ['state', 'used_percent'],
             'regexp': r'(OK|WARNING|CRITICAL): Swap used: ([0-9]+)% .*'
            },         
         ],
        },
    ],


    #changed
    'check_http': [
        {'labelFilter': None,
         'eventtype': 'HTTP',
         'regexps': [
            {'properties': ['url', 'state', 'version', 'status_code', 'status_description', 'bytes', 'response_time'],
             'regexp': r'<A HREF="(.+)" target="_blank">HTTP (OK|WARNING|CRITICAL): HTTP/(\d+.\d+) (\d{3}) (.+) - (\d+) bytes in (\d+.\d+) second response time </A>'
            },
            {'properties': ['state', 'version', 'status_code', 'status_description', 'bytes', 'response_time'],
             'regexp': r'HTTP (OK|WARNING|CRITICAL): HTTP/(\d+.\d+) (\d{3}) (.+) - (\d+) bytes in (\d+.\d+) second response time'
            },
            {'properties': ['state', 'status', 'bytes', 'response_time'],
             'regexp': r'HTTP (OK|WARNING|CRITICAL): Status line output matched "([0-9]+)" - ([0-9]+) bytes in ([0-9.]+) second response time'
            },
            {'properties': ['url', 'state', 'status_description'],
             'regexp': r'<A HREF="([^"]+)" target="_blank">HTTP (.+) - (.+)'
            },
            {'properties': ['state', 'certificate_expiration_date'],
             'regexp': r'(OK|WARNING) - Certificate will expire on (.+)'
            },
         ]
        }
    ],

    'check_ftp': [
        {'labelFilter': None,
         'eventtype': 'FTP',
         'regexps': [
            {'properties': ['state', 'response_time', 'port'],
             'regexp': r"FTP (OK|WARNING|CRITICAL) - (\d+.\d+) seconds? response time on port (\d+)"
            }
         ]
        }
    ],

    # changed
    'check_tcp': [
        {'labelFilter': None,
         'eventtype': 'TCP',
         'regexps': [
            {'properties': ['state', 'response_time', 'port'],
             'regexp': r"TCP (OK|WARNING|CRITICAL) - (\d+.\d+) seconds? response time on port (\d+)"
            },
            {'properties': ['state'],
             'regexp': r"TCP (OK|WARNING|CRITICAL) - Invalid"
            },
         ]
        },
    ],

    #changed
    'host' : [
        {'labelFilter': None,
         'eventtype' : 'Ping',
         'regexps': [
            {'properties': ['state', 'ip', 'loss', 'rta'],
             'regexp': r"FPING (OK|WARNING|CRITICAL) - ([0-9.]+) \(loss=([\d\.]+)%, rta=(\d+\.\d*) ms\)"
            },
            {'properties': ['state', 'ip', 'loss'],
             'regexp': r"FPING (OK|WARNING|CRITICAL) - ([0-9.]+) \(loss=([\d\.]+)%\)"
            },
            {'properties': ['state', 'loss', 'rta'],
             'regexp': r"PING (OK|WARNING|CRITICAL) - Packet loss = ([0-9.]+)%, RTA = ([0-9.]+) ms"
            },
            {'properties': ['state', 'host'],
             'regexp': r'(OK|WARNING|CRITICAL) - Host Unreachable \((.+)\) - host check'}
         ],
        }
    ],


    'check_load': [
        {'labelFilter': None,
         'eventtype': 'Load',
         'regexps': [
            {'properties': ['state', 'min1', 'min5', 'min15'],
             'regexp': r"(OK|WARNING|CRITICAL) - load average: ([0-9.]+), ([0-9.]+), ([0-9.]+)"
            }
         ]
        }
    ],


    'check_cpu': [
        {'labelFilter': None,
         'eventtype': 'CPU',
         'regexps': [
            {'properties': ['state', 'min1', 'min5', 'min15'],
             'regexp': r"(OK|WARNING|CRITICAL) - load average: ([0-9.]+), ([0-9.]+), ([0-9.]+)"
            },
            {'properties': ['state', 'percentual', 'type'],
             'regexp': r"(OK|WARNING|CRITICAL) - CPU em (\d+)%, tipo: (.+)"
            },
            {'properties': ['load', 'time', 'resolution'],
             'regexp': r'CPU Load (\d+)% \((\d+) (\w+) average\)'
            },
         ]
        }
    ],


    'check_cputime': [
        {'labelFilter': None,
         'eventtype': 'CPUSimple',
         'regexps': [
            {'properties': ['state', 'usage'],
             'regexp': r"CPU (OK|WARNING|CRITICAL) - Processor Time= (\d+(?:.\d+)?) %"
            }
         ],
        },
    ],


    'check_dns': [
        {'labelFilter': None,
         'eventtype': 'DNS',
         'regexps': [
            {'properties': ['state', 'response_time', 'domain', 'ip'],
             'regexp': r"DNS (OK|WARNING|CRITICAL): (\d+.\d+) seconds? response time. (.+) returns (.+)"
            }
         ],
        },
    ],


    'check_cpu_snmp': [
        {'labelFilter': None,
         'eventtype': 'CPU',
         'regexps': [
            {'properties': ['state', 'percentual', 'type'],
             'regexp': r"(OK|WARNING|CRITICAL) - CPU em (\d+)%, tipo: (.+)"
            }
         ]
        }
    ],


    'check_fping': [
        {'labelFilter': None,
         'eventtype': 'Ping',
         'regexps': [
            {'properties': ['state', 'ip', 'loss', 'rta'],
             'regexp': r"FPING (OK|WARNING|CRITICAL) - ([0-9.]+) \(loss=([\d\.]+)%, rta=(\d+\.\d*) ms\)"
            },
            {'properties': ['state', 'ip', 'loss'],
             'regexp': r"FPING (OK|WARNING|CRITICAL) - ([0-9.]+) \(loss=([\d\.]+)%\)"
            }
         ]
        }
    ],


    'check_ping': [
        {'labelFilter': None,
         'eventtype': 'Ping',
         'regexps': [
            {'properties': ['state', 'loss', 'rta'],
             'regexp': r"PING (OK|WARNING|CRITICAL) - Packet loss = ([0-9.]+)%, RTA = ([0-9.]+) ms"
            }
         ]
        }
    ],


    'check_procs': [
        {'labelFilter': None,
         'eventtype': 'Procs',
         'regexps': [
            {'properties': ['state', 'number_of_processes', 'args'],
             'regexp': r'(OK|WARNING|CRITICAL) - ([0-9]+) processes running with args (.+)'
            }
         ]

        }
    ],


    'check_local_procs': [
        {'labelFilter': None,
         'eventtype': 'Procs',
         'regexps': [
            {'properties': ['state', 'number_of_processes', 'state_of_process'],
             'regexp': r'PROCS (OK|WARNING|CRITICAL): ([0-9]+) processes with STATE = (.+)'
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

    'check_disk': [
        {'labelFilter': None,
         'eventtype': 'Disk',
         'regexps': [
            {'properties': ['state', 'free_space' , 'usage'],
             'regexp': r'Disk space (OK|WARNING|CRITICAL) - (\d+) kB free \( (\w+) % used\) .*'
            },
            {'properties': ['total', 'total_unit', 'used', 'used_unit', 'used_percentage', 'free', 'free_unit', 'free_percentage'],
             'regexp': r'[cd]:\\ - total: ([\d.]+) (\w{2}) - used: ([\d.]+) (\w{2}) \((\d+)%\) - free ([\d.]+) (\w{2}) \((\d+)%\)'
            },
            {'properties': ['state', 'mount_point', 'free_space_in_mb', 'free_space_percentage', 'inode_percentage', 'mount_point2', 'free_space_in_mb2', 'free_space_percentage2', 'inode_percentage2'],
             'regexp': r'DISK (OK|WARNING|CRITICAL) - free space: ([^\s]+) (\d+) MB \((\d+)% inode=(\d+)%\): ([^\s]+) (\d+) MB \((\d+)% inode=(\d+)%\):'
            },
            {'properties': ['state', 'mount_point', 'free_space_in_mb', 'free_space_percentage', 'inode_percentage'],
             'regexp': r'DISK (OK|WARNING|CRITICAL) - free space: ([^\s]+) (\d+) MB \((\d+)% inode=(\d+)%\):'
            },
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


    'check_heartbeat': [
        {'labelFilter': None,
         'eventtype': 'Heartbeat',
         'regexps': [
            {'properties': ['status', 'mode'],
             'regexp': r'Heartbeat (OK|WARNING|CRITICAL) - Modo (.+)'
            }
         ]
        }
    ],

    'check_nt': [
        {'labelFilter': None,
         'eventtype': 'NSClient',
         'regexps': [
            {'properties': ['ns_version', 'date'],
             'regexp': r'NSClient\+\+ ([\d.]+) ([\d-]+)'
            },
            {'properties': [],
             'regexp': r'could not fetch information from server'
            },
            {'properties': [],
             'regexp': r'No data was received from host!'
            },
            {'properties': [],
             'regexp': r"NSClient - ERROR: Could not get data for 5 perhaps we don't collect data this far back"
            },
            {'properties': [],
             'regexp': r"NSClient - ERROR: Could not get value"
            },
            {'properties': [],
             'regexp': r"NSClient - ERROR: Failed to get PDH value."
            },
            {'properties': ['service','status'],
             'regexp': r"(.+): (Started|Running|Stopped|not running)\s*\z"
            },
            {'properties': ['state'],
             'regexp': r"(OK): All processes are running."
            },
         ]
        }
    ],

    #changed
    'check_mysql': [
        {'labelFilter': None,
         'eventtype': 'MySQL',
         'regexps': [
            {'properties': ['uptime', 'threads', 'questions', 'slow_queries', 'opens', 'flush_tables', 'open_tables', 'average_queries_per_second'],
             'regexp': r'Uptime: ([0-9]+).*?Threads: ([0-9]+).*?Questions: ([0-9]+).*?Slow queries: ([0-9]+).*?Opens: ([0-9]+).*?Flush tables: ([0-9]+).*?Open tables: ([0-9]+).*?Queries per second avg: ([0-9.]+)'
            }
         ]
        }
    ],


    #changed
    'check_mysql_nrpe': [
        {'labelFilter': None,
         'eventtype': 'MySQL',
         'regexps': [
            {'properties': ['uptime', 'threads', 'questions', 'slow_queries', 'opens', 'flush_tables', 'open_tables', 'average_queries_per_second'],
              'regexp': r'Uptime: ([0-9]+).*?Threads: ([0-9]+).*?Questions: ([0-9]+).*?Slow queries: ([0-9]+).*?Opens: ([0-9]+).*?Flush tables: ([0-9]+).*?Open tables: ([0-9]+).*?Queries per second avg: ([0-9.]+)'
            }
         ]
        }
    ],


    'check_dns_stats': [
        {'labelFilter': None,
         'eventtype': 'DNSStats',
         'regexps': [
            {'properties': ['state', 'success', 'referral', 'nxrrset', 'nxdomain', 'recursion', 'failure', 'duplicate', 'dropped','soa','a','ns','cname','ptr','mx','txt','aaaa'],
             'regexp': r'(OK|WARNING|CRITICAL): success: ([0-9]+), referral: ([0-9]+), nxrrset: ([0-9]+), nxdomain: ([0-9]+), recursion: ([0-9]+), failure: ([0-9]+), duplicate: ([0-9]+), dropped: ([0-9]+), soa: ([0-9]+), a: ([0-9]+), ns: ([0-9]+), cname: ([0-9]+), ptr: ([0-9]+), mx: ([0-9]+), txt: ([0-9]+), aaaa: ([0-9]+)'
            }
         ]
        }
    ],


    'check_rrdtraf': [
        {'labelFilter': None,
         'eventtype': 'Traffic',
         'regexps': [
            {'properties': ['interface', 'state', 'in', 'out'],
             'regexp': r'(.+) - (OK|WARNING|CRITICAL) - Current BW in: ([0-9.]+).bps Out: ([0-9.]+).bps'
            }
         ]
        }
    ],


    'check_sessao_vip': [
        {'labelFilter': None,
         'eventtype': 'VIP',
         'regexps': [
            {'properties': ['state', 'site', 'sessions'],
             'regexp': r'(OK|WARNING|CRITICAL): (.+) - (\d+) sessoes abertas'
            }
         ]
        }
    ],


    'check_sessao_vip_temp': [
        {'labelFilter': None,
         'eventtype': 'VIP',
         'regexps': [
            {'properties': ['state', 'site', 'sessions'],
             'regexp': r'(OK|WARNING|CRITICAL): (.+) - (\d+) sessoes abertas'
            }
         ]
        }
    ],


    'check_snmp_streamsess': [
        {'labelFilter': None,
         'eventtype': 'SNMPServerSessions',
         'regexps': [
            {'properties': ['state', 'total'],
             'regexp': r'SNMP (OK|WARNING|CRITICAL) - (.+)'
            }
         ]
        }
    ],


    'check_varnish_client': [
                {'labelFilter': None,
                 'eventtype': 'VarnishClient',
                 'regexps': [
                    {'properties': ['connections', 'connections_per_second',
                                    'dropped', 'dropped_per_second', 'requests',
                                    'requests_per_second'],
                     'regexp': r'Client - Connections: ([0-9]+) \(([0-9.]+)\), Drop: ([0-9]+) \(([0-9.]+)\), Requests: ([0-9]+) \(([0-9.]+)\)',
                    },
                 ],
                },
            ],

    #changed
    'check_varnish_cache': [
        {'labelFilter': None,
         'eventtype': 'VarnishCache',
         'regexps': [
            {'properties': ['hits', 'hits_per_second', 'hitpasses',
                            'hitpasses_per_second', 'misses',
                            'misses_per_second'],
             'regexp': r'Cache Utilization - hit: ([0-9]+) \(([0-9.]+|nan)\), hitpass: ([0-9]+) \(([0-9.]+|nan)\), miss: ([0-9]+) \(([0-9.]+|nan)\)',
            },
         ],
        },
    ],


    #changed
    'check_varnish_backend': [
        {'labelFilter': None,
         'eventtype': 'VarnishBackend',
         'regexps': [
            {'properties': ['conn', 'conn_per_second', 'unhealthy',
                            'unhealthy_per_second', 'busy',
                            'busy_per_second', 'fail', 'fail_per_second',
                            'reuse', 'reuse_per_second', 'toolate',
                            'toolate_per_second', 'recycle',
                            'recycle_per_second', 'unused',
                            'unused_per_second'],
             'regexp': r'Backend Usage - Conn: ([0-9]+) \(([0-9.]+)\), Unhealthy: ([0-9]+) \(([0-9.]+)\), Busy: ([0-9]+) \(([0-9.]+)\), Fail: ([0-9]+) \(([0-9.]+)\), Reuse: ([0-9]+) \(([0-9.]+)\), TooLate: ([0-9]+) \(([0-9.]+)\), Recycle: ([0-9]+) \(([0-9.]+)\), UnUsed: ([0-9]+) \(([0-9.]+)\)',
            },
            {'properties': ['conn', 'conn_per_second', 'unhealthy',
                            'unhealthy_per_second', 'busy',
                            'busy_per_second', 'fail', 'fail_per_second',
                            'reuse', 'reuse_per_second', 'toolate',
                            'toolate_per_second', 'recycle',
                            'recycle_per_second'],
             'regexp': r'Backend Usage - Conn: ([0-9]+) \(([0-9.]+)\), Unhealthy: ([0-9]+) \(([0-9.]+)\), Busy: ([0-9]+) \(([0-9.]+)\), Fail: ([0-9]+) \(([0-9.]+)\), Reuse: ([0-9]+) \(([0-9.]+)\), TooLate: ([0-9]+) \(([0-9.]+)\), Recycle: ([0-9]+) \(([0-9.]+)\), UnUsed:  \(\)',
            }
         ],
        },
    ],


    'check_home': [
        {'labelFilter': None,
         'eventtype': 'HTTPStats',
         'regexps': [
            {'properties': ['state','ttfb', 'ttime', 'check'],
             'regexp': r'(OK|WARNING|CRITICAL): ttfb: ([0-9.]+) - ttime: ([0-9.]+) - check: ([0-9.]+)',
            },
	 ],
    	},
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

    'check_certificado': [
        {'labelFilter': None,
         'eventtype': 'Certificate',
         'regexps': [
            {'properties': ['state', 'expiration_date'],
             'regexp': r'(OK|WARNING) - Certificate will expire on (.+)'
            },
         ] 
        }
    ],

    'check_CurrentAnonymousUsers': [
        {'labelFilter': None,
         'eventtype': 'IIS_Users',
         'regexps': [
            {'properties': ['number_anonymous_users'],
             'regexp': r'CurrentAnonymousUsers=(\d+)'
            },
         ]
        }
    ],


    'check_CurrentConnections': [
        {'labelFilter': None,
         'eventtype': 'IIS_Connections',
         'regexps': [
            {'properties': ['number_connections'],
             'regexp': r'CurrentConnections=(\d+)'
            },            
         ]
        }
    ],

    'check_msmq': [
        {'labelFilter': None,
         'eventtype': 'MSMQ',
         'regexps': [
            {'properties': ['state','path','num_msg_queue'],
             'regexp': r'(OK|WARNING|CRITICAL): \\MSMQ Queue\((.+)\)\\Messages in Queue: (\d+)'
	        }
         ]
        }
    ],

    'check_whois': [
        {'labelFilter': None,
         'eventtype': 'WHOIS',
         'regexps': [
            {'properties': ['state','domain','days_to_expiration','expiration_date'],
             'regexp': r'(OK) - Dominio: ([\d\w\.]+) com ([\d\.]+) dias para expirar. Expires: (\d{8})'
	        }
         ]
        }
    ],

    'check_lock': [
        {'labelFilter': None,
         'eventtype': 'LOCK',
         'regexps': [
            {'properties': ['lock_type'],
             'regexp': r'([\S]+|OK - have fun)\s*\z'
	        }
         ]
        }
    ],

    'check_query': [
        {'labelFilter': None,
         'eventtype': 'Query',
         'regexps': [
            {'properties': ['state','count_query_args','count_result'],
             'regexp': r'(OK) - select count(.+): ([0-9]+)'
	        }
         ]
        }
    ],

    'check_query_web': [
        {'labelFilter': None,
         'eventtype': 'Query_Web',
         'regexps': [
            {'properties': ['state','query','result'],
             'regexp': r'(OK|WARNING|CRITICAL) - (.+): ([0-9]+)'
	        }
         ]
        }
    ],

    'check_query_duration': [
        {'labelFilter': None,
         'eventtype': 'Query_Duration',
         'regexps': [
            {'properties': ['state','query_duration_time'],
             'regexp': r'(OK|WARNING|CRITICAL): Query duration=([0-9.]+) seconds.'
	        }
         ]
        }
    ],

    'check_solr_jmx': [
        {'labelFilter': None,
         'eventtype': 'Solr',
         'regexps': [
            {'properties': ['jmx_result'],
             'regexp': r'([0-9.]+)'
	        }
         ]
        }
    ],

}


#add common error expressions
errorRegexps = [
    {'properties' : ['description'],
     'regexp' : r"(\(Service Check Timed Out\))"
    },
    {'properties' : ['description'],
     'regexp' : r"(\(Host Check Timed Out\))"
    },
    {'properties' : ['description'],
     'regexp' : r"(CHECK_NRPE)"
    },
    {'properties' : ['description'],
     'regexp' : r"(NRPE: Unable to read output)"
    },
    {'properties' : ['description'],
     'regexp' : r"(Connection refused)"
    },
    {'properties' : ['description'],
     'regexp' : r"(Connection refused by host)" 
    },
    {'properties' : ['state','description'],
     'regexp' : r'(WARNING|CRITICAL) - (Socket timeout after .+ seconds)'
    },
    {'properties' : ['msg_source','timeout_seconds'],
     'regexp' : r'([^:]+): Socket timeout after ([\d.]+) seconds.'
    },
    {'properties' : ['log_file'],
     'regexp' : r'Could not construct return packet in NRPE handler check client side (\(.+\)) logs...'
    },
    {'properties': ['state', 'msg_source', 'unachievable_host_add'],
     'regexp': r'(ERROR): (.+) : No response from remote host "([\d.]+)"\.'
    },
    {'properties': ['description'],
     'regexp': r"(No route to host)"
    },
    {'properties': ['state','description'],
     'regexp': r"(WARNING|CRITICAL) - (Socket timeout)"
    },
    {'properties': ['url', 'status_description'],
     'regexp': r'<A HREF="([^"]+)" target="_blank">(Connection refused)'
    },
    {'properties': ['state', 'connection_not_established_time_window_in_secs'],
     'regexp': r'(CRITICAL) - connection could not be established within ([0-9.]+) seconds'
    },
    {'properties': ['description'],
     'regexp': r'(\(No output returned from plugin\))'
    },
]

expressions['tcp'] = expressions['check_tcp']
expressions['check_local_load'] = expressions['check_load']
expressions['check_local_disk'] = expressions['check_disk']
expressions['check_url'] = expressions['check_http']
expressions['check_https'] = copy.deepcopy(expressions['check_http'])
expressions['check_https'][0]['eventtype'] = 'HTTPS'
expressions['check_http_jetty_admin'] = expressions['check_http']
expressions['check_http_jetty_igimoveis'] = expressions['check_http']
expressions['check_http_solr'] = expressions['check_http']
expressions['http_args_follow'] = expressions ['check_http']
expressions['http_args'] = expressions['check_http']
expressions['https'] = expressions['check_http']
expressions['https_args'] = expressions['check_http']
expressions['http_regexp'] = expressions['check_http']
expressions['check_locks_db'] = expressions['check_lock']

#This is a special case. Events in here are originated from a remote server
#In order to have the correct event label, we use the specific events patterns
#whenever possible (like check_cpu, for instance). Only specific network issues 
#should be directly added to the check_nt patterns like a connection problem pattern
expressions['check_nt'] += expressions['check_cpu'] + expressions['check_mem'] + expressions['check_disk'] + expressions['check_uptime']

