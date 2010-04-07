messages = '''
CHECK_NRPE: Error - Could not complete SSL handshake.
<A HREF="https://something/" target="_blank">CRITICAL - Socket timeout after 10 seconds
Connection refused by host
'''

import sys
sys.path.append('/path/to/neb2activemq/ipc2activemq/src/nebpublisher/utils') 
import topics
import neb_parser


parser_functions = type('empty_class', tuple(), {})
parser_functions.commands = []
my_parser = neb_parser.Parser(topics, parser_functions)

for line in messages.split('\n'):
    if not line:
        continue
    message = 'HOST^%s^STATE^%s' % ('check_cpu', line)
    parsed = my_parser.parse(13, message)
    if parsed != neb_parser.BAD_FORMAT:
        print line, parsed
    else:
         print 'NOT PARSED: %s' % message
    print ''
