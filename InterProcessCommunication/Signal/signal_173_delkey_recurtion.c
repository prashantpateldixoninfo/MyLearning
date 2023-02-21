#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

void abc(int signo)
{
	printf("You have pressed the DEL<ctrl + c> key with signo %d\n", signo);
	signal(SIGINT, abc);
}

int main()
{
	printf("Press DEL<ctrl + c> key\n");
	signal(SIGINT, abc); // key, function
	for(;;);
	return 0;
}
