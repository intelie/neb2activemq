#!/bin/bash

cd ..
mkdir -p dist
tar -czvf dist/neb2ipc.tar.gz src/Makefile src/neb2ipc.c src/include/*.h scripts/install.sh
