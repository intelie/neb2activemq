#!/bin/bash
#
# File: find_messages.sh
# Find messages with a given pattern
#

if [ "$#" -lt "1" ]; then
    echo "Provide a message pattern. Aborting."
    exit -1
fi
grep -oC 2 -E "Type: 1(3|4) Message:.*" nebpublisher.log  | grep -E $1 | cut -d' ' -f 4-50

