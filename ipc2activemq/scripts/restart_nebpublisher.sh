sudo kill -9 `ps aux | grep nebpublisher.py | grep -v grep | awk {'print $2'}`
sudo python nebpublisher.py
