#!/bin/bash


NAGIOS_PATH="/usr/local/nagios"
NAGIOS_DAEMON="/etc/init.d/nagios"
NEB2IPC_DIR="."
NAGIOS_BIN="${NAGIOS_PATH}/bin"
NAGIOS_CFG="${NAGIOS_PATH}/etc/nagios.cfg"
LINE_TO_ADD="broker_module=${NAGIOS_BIN}/neb2ipc.o"


#NEB2IPC COMPILATION
cd $NEB2IPC_DIR
echo "[EXECUTING MAKE...]"
make


#TODO: check if .o was successfully generated.
echo "[MOVING OBJECT FILE neb2ipc.o]"
sudo cp neb2ipc.o $NAGIOS_BIN


#UPDATES NAGIOS.CFG
NEB2IPC_COMMENT=`cat $NAGIOS_CFG | grep -on "#broker_module.*neb2ipc.o"`
if [ -n "$NEB2IPC_COMMENT" ]
then
  echo "[FOUND A COMMENTED LINE FOR neb2ipc.o BROKER. REMOVING.]"
  sudo sed -i "/^#broker_module.*neb2ipc.o/d" $NAGIOS_CFG
fi

NEB2IPC_LINE=`cat $NAGIOS_CFG | grep -on "broker_module.*neb2ipc.o" | cut -d: -f1`
if [ -z "$NEB2IPC_LINE" ] 
then
	BROKER_LINE=`cat $NAGIOS_CFG | grep -no "broker_module=" | cut -d: -f1 | tail -1`
  if [ -n "$BROKER_LINE" ]
  then
    echo "[ADDING neb2ipc.o reference INTO nagios.cfg]"
    sudo sed -i "${BROKER_LINE}a${LINE_TO_ADD}" $NAGIOS_CFG
  else
    echo "[BROKER_MODULE SESSION NOT FOUND. ABORTING.]"
    exit -1
  fi
else
  echo "[REFERENCE TO neb2ipc.o FOUND]"
fi


#RESTARTS NAGIOS
echo "[RESTARTING NAGIOS]"
sudo ${NAGIOS_DAEMON} restart


#SIMPLE CHECK IF WAS SUCCESSFUL
QUEUE_EXISTS=`sudo ipcs | grep "0x0001e240.*nagios"` 
if [ -n "$QUEUE_EXISTS" ]
then
  echo "[MESSAGE QUEUE CREATED SUCCESSFULLY!]"
  echo "[NEB2IPC SEEMS TO BE CORRECTLY INSTALLED. ENJOY!]"
  exit 0
else
  echo "[MESSAGE QUEUE NOT FOUND.]"
fi
