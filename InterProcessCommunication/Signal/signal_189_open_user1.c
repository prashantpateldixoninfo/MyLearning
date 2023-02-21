#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

int pid, i;

void abc(int signo)
{
	printf("\n******** i is %d***********\n", i);
}

int main()
{
	pid = fork();
	if(pid == 0)
	{
		sleep(1);
		printf("Child process with pid %d and ppid %d\n", getpid(), getppid());
		kill(getppid(), SIGUSR1);
		exit(0);
	}
	else
	{
		signal(SIGUSR1, abc);
		for(i=0;i<1000;i++)
			printf("%d..\t",i);
		sleep(1);
		printf("parent exiting\n");
	}
	return 0;
}
