#!/bin/bash
#
# File: not_registered.sh
# Description: find checks without conf (not present in topics.py) 
#

grep -oE "Event (.*) not registered as a topic" nebpublisher_parser.log | awk {'print $3'} | sort | uniq
