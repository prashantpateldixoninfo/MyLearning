/* Let see that how zombie processwill be created by below code in process 
   table */

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
		printf("first-child terminating from memory\n");
	}
	else
	{
		sleep(1);
		int dip = fork();
		if(dip == 0) // second child process
		{
			printf("2nd child's process id is %d\n", getpid());
			printf("second-child terminating\n");
		}
		else
		{
			sleep(15);
			printf("Child with pid %d died\n", wait(0));
			printf("Child with pid %d died\n", wait(0));
			printf("I m parent and I am dying\n");
		}
	}
	return 0;
}
