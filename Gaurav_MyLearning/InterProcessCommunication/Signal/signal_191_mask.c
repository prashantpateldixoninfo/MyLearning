#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

void abc(int signo)
{
	if(signo == SIGINT)
		printf("This is function handler for \"Ctrl + c\"\n");
	if(signo == SIGQUIT)
		printf("This is function handler for \"Ctrl + \\\"\n");
}

int main()
{
	int oldmask;
	char i = 0;
	system("clear");
	oldmask = sigblock(sigmask(SIGINT) | sigmask(SIGQUIT));
	signal(SIGINT, abc);
	signal(SIGQUIT, abc);

	/* This is the crutial area that will be blocked for signals SIGINT & SIGQUIT */
	while(i <= 3)
	{
		printf("Sleep and id is %d\n", getpid());
		sleep(1);
		i++;
	}

	sigsetmask(oldmask);

	/* This function will realeses the functions */
	while(i <= 5)
	{
		printf("This is after the releasing the SIGNALS\n");
		sleep(1);
		i++;
	}
	return 0;
}
