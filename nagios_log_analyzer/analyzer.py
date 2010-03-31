#!/usr/bin/python

import sys

if len(sys.argv) < 2:
    print 'Usage: %s <Nagios log filename> [CSV filename]' % sys.argv[0]
    print "If you don't specify [CSV filename], it'll be outputed"
    sys.exit(1)

CSV_filename_was_specified = len(sys.argv) > 2

try:
    log = open(sys.argv[1], 'r')
except IOError:
    print "IOError: can't open filename \"%s\" for reading." % sys.argv[1]
    sys.exit(1)

result = []
for line in log:
    line_by_spaces = line.split()
    if ' '.join(line_by_spaces[1:3]) == 'SERVICE ALERT:' or \
       ' '.join(line_by_spaces[1:3]) == 'HOST ALERT:' or \
       ' '.join(line_by_spaces[1:4]) == 'CURRENT HOST STATE:' or \
       ' '.join(line_by_spaces[1:4]) == 'CURRENT SERVICE STATE:':
       fields = line.split(';')
       command_line = fields[1]
       output = line[line.rfind(';') + 1:].replace('\n', '')
       result.append((command_line, output))

result = set(result) #remove duplicates

if CSV_filename_was_specified:
    try:
        csv_file = open(sys.argv[2], 'w')
    except IOError:
        print "IOError: can't open filename \"%s\" for writing." % sys.argv[2]
        sys.exit(1)
    csv_file.write('"Command Name","Output"\n')
    csv_file.write('\n'.join(['"%s","%s"' % (line[0], line[1]) for line in result]))
else:
    print '\n'.join(['%s: %s' % (line[0], line[1]) for line in result])
