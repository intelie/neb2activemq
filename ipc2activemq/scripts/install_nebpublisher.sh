cd ../src/
sudo -u nagios python2.6 setup.py install
if [ $? != 0 ]
then
  echo "[NEBPUBLISHER NOT INSTALLED. ABORTING.]"
else
  echo "[NEBPUBLISHER SUCCESSFULLY INSTALLED.]"
fi

