#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

int pid;

void abc(int signo)
{
	sleep(1);
	printf("Bye Dad\n");
	exit(0);
}

void def(int signo)
{
	sleep(1);
	printf("Hello Baby\n");
	kill(pid, SIGUSR2);
}

int main()
{
	pid = fork();
	if(pid == 0)
	{
		signal(SIGUSR2, abc);
		sleep(1);
		printf("Hello Dad\n");
		kill(getppid(), SIGUSR1);
		sleep(5);
	}
	else
	{
		signal(SIGUSR1, def);
		sleep(5);
	}
	return 0;
}
