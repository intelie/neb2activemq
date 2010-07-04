###################################
# Makefile for NEB Intelie
#
###################################


# Source code directories
SRC_INCLUDE=./include

CC=gcc
MOD_CFLAGS=-fPIC
CFLAGS=-g -O2 -DHAVE_CONFIG_H
MOD_LDFLAGS=-shared
LDFLAGS=
LIBS=
DBG_FLAGS= -DDEBUG=1

CP=@CP@

all: neb2ipc

debug: neb2ipc_debug

neb2ipc: neb2ipc.c
	$(CC) $(MOD_CFLAGS) $(CFLAGS) -combine -o neb2ipc.o neb2ipc.c $(MOD_LDFLAGS) $(LDFLAGS) $(LIBS)

neb2ipc_debug: neb2ipc.c
	$(CC) $(MOD_CFLAGS) $(CFLAGS) $(DBG_FLAGS) -combine -o neb2ipc.o neb2ipc.c $(MOD_LDFLAGS) $(LDFLAGS) $(LIBS)

clean:
	rm -f neb2ipc.o
	rm -f *~ *.*~

distclean: clean
	rm -f Makefile

devclean: distclean

install:

	
