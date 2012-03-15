#!/bin/bash

# SCRIPT FOR PYTHON 2.6 INSTALLATION
# TODO: validate this script on CENTOS



#SMOKE TESTING FOR PYTHON 2.6
which python2.6 &>/dev/null
if [ $? = 0 ] 
then
  echo "[PYTHON 2.6 ALREADY INSTALLED]"
else
  echo "[PYTHON 2.6 NOT FOUND]"
  echo "[INSTALLING PYTHON 2.6]"
  cd /home/intelie/neb2activemq/ipc2activemq/lib
  tar -xzf Python-2.6.5.tgz
  cd Python-2.6.5
  ./configure
  make
  sudo make altinstall 
  cd /home/intelie/neb2activemq/ipc2activemq/scripts
  if [ $? = 0 ]
  then
    which python2.6 &>/dev/null
    if [ $? = 0 ]
    then 
      echo "[PYTHON2.6 INSTALLED SUCCESSFULLY!]"
      exit 0
    else
      exit -1 
    fi
  fi
fi
