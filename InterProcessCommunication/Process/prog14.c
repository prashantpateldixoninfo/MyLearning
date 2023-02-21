/* The way to find the parent id of child process and parent process.
   parent's parent id would be bash shell id "ps -e" */

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
	}
	else
	{
		sleep(1);
		printf("I am the parent, my Process ID is %d\n", getpid());
		printf("The parent's parent process ID is %d\n", getppid());
	}
		
	return 0;
}
