#!/bin/sh

# collect information
REP=1800
INT=1

mkdir target
rm target/output.dat
rm fakenagios.dat
touch target/output.dat

sar -x `cat /usr/local/nagios/var/nebpublisher.pid` $INT $REP | ./stat2plot_sar.pl > target/output.dat &

echo "Collecting..."

sudo -u nagios python fakenagios.py

echo "Fake nagios ended."
echo "Please turn off sar manually."