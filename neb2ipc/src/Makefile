###################################
# Makefile for NEB Intelie
#
###################################


# Source code directories
SRC_INCLUDE=./include

CC=gcc
MOD_CFLAGS=-fPIC
CFLAGS=-g -O2 -DHAVE_CONFIG_H -DNSCORE
MOD_LDFLAGS=-shared
LDFLAGS=
LIBS=
DBG_FLAGS= -DDEBUG=1
TESTING_FLAGS = -lcmockery -std=c99

CP=@CP@

all: neb2ipc test
	sudo ipcrm -Q 123456
	./test
	sudo ipcrm -Q 123456

debug: neb2ipc_debug

neb2ipc: neb2ipc.c
	$(CC) $(MOD_CFLAGS) $(CFLAGS) -o neb2ipc.o neb2ipc.c $(MOD_LDFLAGS) $(LDFLAGS) $(LIBS)

neb2ipc_debug: neb2ipc.c
	$(CC) $(MOD_CFLAGS) $(CFLAGS) $(DBG_FLAGS) -o neb2ipc.o neb2ipc.c $(MOD_LDFLAGS) $(LDFLAGS) $(LIBS)

test: unitTests.c neb2ipc.c
	$(CC) $(CFLAGS) -o test neb2ipc.c unitTests.c $(TESTING_FLAGS) 

clean:
	rm -f neb2ipc.o
	rm -f *~ *.*~
	rm -f test

distclean: clean
	rm -f Makefile

devclean: distclean

install:

	
