# IPC2ACTIVEMQ INSTALLATION

./install_python.sh
if [ $? != 0 ]
then
  echo "[PYTHON NOT INSTALLED. ABORTING.]"
else
  sudo -u nagios python2.6 install_dependencies.py
  if [ $? != 0 ]
  then
    echo "[PYTHON DEPENDENCIES NOT INSTALLED. ABORTING.]"
  else
    sudo -u nagios python2.6 install_nebpublisher.sh
    if [ $? != 0 ]
    then
      echo "[DAEMON NOT INSTALLED. ABORTING.]"
    else
      echo "[NEBPUBLISHER DAEMON INSTALLED.]"
      echo "[IPC2ACTIVEMQ INSTALLED.]"
    fi
  fi
fi
