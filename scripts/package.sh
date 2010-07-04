#!/bin/bash

# SCRIPT TO PACKAGE NEB2ACTIVEMQ

mkdir -p ../dist/neb2ipc
mkdir -p ../dist/ipc2activemq

cd ../neb2ipc/scripts
./package.sh
cp ../dist/*.tar.gz  ../../dist/neb2ipc

cd ../../ipc2activemq/scripts
./package.sh
cp ../dist/*.tar.gz ../../dist/ipc2activemq

cd ../../dist/neb2ipc/
tar -xzvf *.tar.gz
rm -rf *.tar.gz

cd ../../dist/ipc2activemq
tar -xzvf *.tar.gz
rm -rf *.tar.gz

cd ..
mkdir -p neb2activemq/scripts
cp ../scripts/install.sh neb2activemq/scripts/

cp -r neb2ipc ipc2activemq neb2activemq
tar -czvf neb2activemq.tar.gz neb2activemq
rm -rf neb2activemq ipc2activemq neb2ipc scripts
