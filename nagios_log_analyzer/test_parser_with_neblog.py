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

for message in messages.split('\n'):
    if not message:
        continue
    parsed = my_parser.parse(13, message)
    if parsed != neb_parser.BAD_FORMAT and parsed != neb_parser.NOT_IMPLEMENTED:
        print line, parsed
    else:
         print 'NOT PARSED: %s' % message

messages_file_object.close()
