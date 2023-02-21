/* The way to see the "orphan" status in process table id "ps -el" */

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
		sleep(15);
		printf("I am the child, my Process ID is %d\n", getpid());
		printf("The child's parent process ID is %d\n", getppid());
	}
	else
	{
		sleep(5);
		printf("I am the parent, my Process ID is %d\n", getpid());
		printf("The parent's parent process ID is %d\n", getppid());
	}
		
	return 0;
}
