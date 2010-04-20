import sys
sys.path.append('../ipc2activemq/src/nebpublisher/utils')
sys.path.append('/home/intelie/igsetup/trunk')
filename = '/home/intelie/igsetup/trunk/v4/final.txt'
parser_functions_path = '../ipc2activemq/src/nebpublisher/conf/dev/'

import topics
import neb_parser
import imp

parser_functions_fp = open(parser_functions_path + 'parser_functions.py', 'rb')
parser_functions = imp.load_source("parser_functions", parser_functions_path,
                                   parser_functions_fp)

my_parser = neb_parser.Parser(topics, parser_functions)

messages_file_object = open(filename)
messages = messages_file_object.read()

parsed_fp = open('parsed.txt', 'w')
not_parsed_fp = open('not_parsed.txt', 'w')

total = 0
total_parsed = 0
total_not_parsed = 0
for message in messages.split('\n'):
    if not message:
        continue
    parsed = my_parser.parse(13, message)
    if parsed == neb_parser.BAD_FORMAT or parsed == neb_parser.NOT_IMPLEMENTED:
        not_parsed_fp.write('ERROR: Message: "%s" - Returned code: %d\n' % (message, parsed))
        total_not_parsed += 1
    else:
        parsed_fp.write('%s\n%s\n\n' % (message, str(parsed)))
        total_parsed += 1
    total += 1

total = float(total) / 100
print 'Total parsed: %d (%2.2f%%)' % (total_parsed, total_parsed / total)
print 'NOT PARSED: %d (%2.2f%%)' % (total_not_parsed, total_not_parsed / total)

messages_file_object.close()
parsed_fp.close()
not_parsed_fp.close()
