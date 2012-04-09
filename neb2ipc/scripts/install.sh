#!/bin/bash

# NEB2IPC MODULE
# INSTALLATION SCRIPT FROM THE SOURCE CODE


#PATHS RECOMMENDED BY NAGIOS DOCUMENTATION. CHANGE THESE IF NECESSARY
NAGIOS_PATH="/usr"
NAGIOS_DAEMON="/etc/init.d/nagios"
NEB2IPC_DIR="../src"
NAGIOS_BIN="${NAGIOS_PATH}/bin"
NAGIOS_CFG="/etc/nagios/nagios.cfg"
LINE_TO_ADD="broker_module=${NAGIOS_BIN}/neb2ipc.o"


#SMOKE TESTING
if [ ! -f "${NAGIOS_PATH}/bin/nagios" ]
then
  echo "[Nagios binary not found in ${NAGIOS_PATH}/bin]"
  echo "[HAVE YOU INSTALLED NAGIOS?]"
  exit -1
fi


#NEB2IPC COMPILATION
cd $NEB2IPC_DIR
echo "[Executing make...]"
make

if [ -f neb2ipc.o ]
then
  echo "[Moving object neb2ipc.o]"
  sudo -u nagios cp neb2ipc.o $NAGIOS_BIN
else
  echo "[File neb2ipc.o not found]"
  echo "[ABORTING]"
  exit -1
fi


#UPDATES NAGIOS.CFG
NEB2IPC_COMMENT=`cat $NAGIOS_CFG | grep -on "#broker_module.*neb2ipc.o"`
if [ -n "$NEB2IPC_COMMENT" ]
then
  echo "[Found a commented line in neb2ipc.o broker, REMOVING]"
  sudo sed -i "/^#broker_module.*neb2ipc.o/d" $NAGIOS_CFG
fi

NEB2IPC_LINE=`cat $NAGIOS_CFG | grep -on "broker_module.*neb2ipc.o" | cut -d: -f1`
if [ -z "$NEB2IPC_LINE" ] 
then
	BROKER_LINE=`cat $NAGIOS_CFG | grep -no "broker_module=" | cut -d: -f1 | tail -1`
  if [ -n "$BROKER_LINE" ]
  then
    echo "[Adding neb2ipc.o reference into nagios.cfg]"
    sudo sed -i "${BROKER_LINE}a${LINE_TO_ADD}" $NAGIOS_CFG
  else
    echo "[Broker module session not found, ABORTING]"
    exit -1
  fi
else
  echo "[Reference to neb2ipc.o already existfound in nagios.cfg]"
fi


#RESTARTS NAGIOS
echo "[RESTARTING NAGIOS]"
sudo ${NAGIOS_DAEMON} restart


#SIMPLE CHECK IF IT WAS SUCCESSFUL
QUEUE_EXISTS=`sudo ipcs | grep "0x0001e240.*nagios"` 
if [ -n "$QUEUE_EXISTS" ]
then
  echo "[MESSAGE QUEUE CREATED SUCCESSFULLY!]"
  echo "[NEB2IPC SEEMS TO BE CORRECTLY INSTALLED, ENJOY!]"
  exit 0
else
  echo "[MESSAGE QUEUE NOT FOUND.]"
  exit -1
fi
