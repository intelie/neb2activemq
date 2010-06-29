#!/bin/bash

mkdir -p dist
tar -czvf dist/neb2ipc.tar.gz Makefile neb2ipc.c include/*.h install.sh
