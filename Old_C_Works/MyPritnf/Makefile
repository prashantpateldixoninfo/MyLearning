# the compiler: gcc for C program, define as g++ for C++
CC=gcc

# compiler flags:
#  -g    adds debugging information to the executable file
#  -Wall turns on most, but not all, compiler warnings
CFLAGS  = -g -Wall

all: 
	$(CC) $(CFLAGS) -o shm_sem_client shm_sem_client.c shm_sem_util.c
	$(CC) $(CFLAGS) -o shm_sem_server shm_sem_server.c shm_sem_util.c

clean:
	rm -rf shm_sem_client shm_sem_server
