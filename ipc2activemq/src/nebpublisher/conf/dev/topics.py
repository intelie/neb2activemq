

#Defines topics of interests to log from nagios and their regexps

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
  },
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
        ]
}
