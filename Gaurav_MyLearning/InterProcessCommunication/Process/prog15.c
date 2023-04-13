/* Below programm define the oprphan process scenario.
   Since, parent process terminate early then child process therefore,
   Child process assigned id as 1. which is id of "process dispatcher" i.e. 
   "init" */

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
	int pid = fork();
	
	if(pid == 0)
	{
		printf("I am the child, my Process ID is %d\n", getpid());
		printf("The child's parent process ID is %d\n", getppid());
		sleep(5);
		printf("I am the child, my Process ID is %d\n", getpid());
		printf("The child's parent process ID is %d\n", getppid());
	}
	else
	{
		sleep(1);
		printf("I am the parent, my Process ID is %d\n", getpid());
		printf("The parent's parent process ID is %d\n", getppid());
	}
		
	return 0;
}
