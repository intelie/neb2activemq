

cd ../neb2ipc/scripts
./install.sh

if [ $? = 0 ]
then
  echo "[NEB2IPC MODULE INSTALLED SUCCESSFULLY]"
else
  echo "[NEB2IPC INSTALLATION ERROR. ABORTING.]"
  exit -1
fi

cd ../../ipc2activemq/scripts
./install.sh

if [ $? = 0 ]
then
  echo "[IPC2ACTIVEMQ MODULE INSTALLED SUCCESSFULLY]"
else
  echo "[IPC2ACTIVEMQ INSTALLATION ERROR. ABORTING.]"
  exit -1
fi

echo "[NEB2ACTIVEMQ INSTALLED SUCCESSFULLY. ENJOY!!!]"
