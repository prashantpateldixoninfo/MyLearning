/* By the use of wait() API we can stopped the child process to become zombie */

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>

int main()
{
	int pid = fork();
	if(pid == 0) // fist child process
	{
		printf("1st child's process id is %d\n", getpid());
		printf("first-child dead\n");
		sleep(5);
	}
	else
	{
		sleep(1);
		int dip = fork();
		if(dip == 0) // second child process
		{
			printf("2nd child's process id is %d\n", getpid());
			printf("second-child dead\n");
			sleep(10);
		}
		else
		{
			int cpid = wait(0);
			printf("Child with pid %d died\n", cpid);
			cpid = wait(0);
			printf("Child with pid %d died\n", cpid);
			printf("I m parent and I am dying\n");
		}
	}
	return 0;
}
