#!/bin/bash

NEB2IPC_DIR="./neb2ipc/"
NAGIOS_BIN="/usr/local/nagios/bin"
NAGIOS_CFG="/etc/nagios3/nagios.cfg"
LINE_TO_ADD="broker_module=${NAGIOS_BIN}/neb2ipc.o"


#NEB2IPC COMPILATION
cd $NEB2IPC_DIR
echo "[EXECUTING MAKE...]"
make

#TODO: checar se o arquivo .o foi gerado com sucesso
echo "[MOVING OBJECT FILE neb2ipc.o]"
cp neb2ipc.o $NAGIOS_BIN

#se não existir, inclui referencia ao broker_module do neb2ipc.o
NEB2IPC_LINE=`cat $NAGIOS_CFG | grep -on "broker_module.*neb2ipc.o" | cut -d: -f1`
if [ -z $NEB2IPC_LINE ] 
then
	BROKER_LINE=`cat $NAGIOS_CFG | grep -no "broker_module=" | cut -d: -f1 | head -1`

	if [ -n $BROKER_LINE ]
	then
		echo "[ADDING neb2ipc.o reference INTO nagios.cfg]"
		sed -i "${BROKER_LINE}a${LINE_TO_ADD}" $NAGIOS_CFG
	fi
fi

