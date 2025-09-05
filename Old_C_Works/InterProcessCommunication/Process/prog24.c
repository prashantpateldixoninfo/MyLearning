/* How to make parent wait for more than one child. Here we can see that two
   entry of zombie process in process table */

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
	}
	else
	{
		sleep(1);
		int dip = fork();
		if(dip == 0) // second child process
		{
			printf("2nd child's process id is %d\n", getpid());
			printf("second-child dead\n");
		}
		else
		{
			sleep(15);
			printf("I am parent and I am dying\n");
		}
	}
	return 0;
}
