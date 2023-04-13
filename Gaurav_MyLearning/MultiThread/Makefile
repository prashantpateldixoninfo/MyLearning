CC=gcc

*.o:*.c
	$(CC) -c -o $@ $<

multithread_simple: multithread_simple.o
	$(CC) -o multithread_simple multithread_simple.o

multithread_mutex: multithread_mutex.o
	$(CC) -o multithread_mutex multithread_mutex.o

all: multithread_simple multithread_mutex

clean:
	rm -rf *.o  multithread_simple multithread_mutex 

