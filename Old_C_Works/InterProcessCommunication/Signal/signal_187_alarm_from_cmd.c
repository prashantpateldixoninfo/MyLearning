#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>

char msg[100];

void abc(int signo)
{
	printf("%s\n", msg);
	exit(0);
}

int main(int argc, char *argv[])
{
	if(argc < 3 || argc > 3)
	{
		perror("Usage: filename [message] [alarm timeout]\n");
		return -1;
	}
	int tim = atol(argv[2]);
	strcpy(msg, argv[1]);
	signal(SIGALRM, abc);
	alarm(tim);
	for(;;);
	return 0;
}
