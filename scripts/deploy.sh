./package.sh
ssh root@nagios 'cd /opt/intelie; rm -rf neb*'
scp ../dist/neb2activemq*.tar.gz root@nagios:/opt/intelie
ssh root@nagios 'cd /opt/intelie; tar zxf neb2activemq*.tar.gz; rm -rf neb2activemq*.tar.gz' 
