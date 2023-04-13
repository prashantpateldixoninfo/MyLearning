/* This programm will create a zombie process. where the child process will die first and 
 * when parent process is excuted it will show the process table we can see the entry
 * for zombie process. 
 */
 
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void)
{
	int pid;
	pid = fork();
	if (pid == 0)
	{
		printf("Child Process with id = %d\n", getpid());	// Child Process
		exit(0);
	}
	else
	{
		/* The Parent is made to sleep so that the parent dies */
		printf("Parent Process with id = %d\n", getpid());
		sleep(5);
		system("ps -al");
		sleep(5);
	}
	return 0;
}


