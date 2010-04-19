import sys
sys.path.append('../ipc2activemq/src/nebpublisher/utils')
sys.path.append('/home/alvaro/Intelie/Code/igsetup/trunk')
filename = '/home/alvaro/Intelie/Code/igsetup/trunk/v4/final.txt'

import topics
import neb_parser


parser_functions = type('empty_class', tuple(), {})
parser_functions.commands = []
my_parser = neb_parser.Parser(topics, parser_functions)

messages_file_object = open(filename)
messages = messages_file_object.read()

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

messages_file_object.close()
