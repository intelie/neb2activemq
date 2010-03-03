
sudo -u nagios cp neb2ipc.o /usr/local/nagios/bin/;

sudo /etc/init.d/nagios restart

tail -200f /usr/local/nagios/var/nagios.log

