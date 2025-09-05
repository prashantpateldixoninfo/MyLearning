CC=gcc

*.o:*.c
	$(CC) -c -o $@ $<

server: server.o
	$(CC) -o server server.o

client: client.o
	$(CC) -o client client.o

all: server client

clean:
	rm -rf *.o  server client

