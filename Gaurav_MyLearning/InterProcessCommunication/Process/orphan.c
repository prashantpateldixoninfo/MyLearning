/* Orphan Process */

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main()
{
	int pid;
	pid = fork();
	if (pid == 0)
	{
		/* The child is made to sleep so that the parent dies */
		printf("Child Process with pid = %d and ppid = %d\n", getpid(), getppid());
		sleep(5);
		system ("ps -al");
		printf("Child Process with pid = %d and ppid = %d\n", getpid(), getppid());
		sleep(5);
	}
	else
	{
		printf("Parent Process with pid = %d\n", getpid());		// Parent Process
		exit(0);
	}
	return 0;
}
