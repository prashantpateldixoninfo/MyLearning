/* The way to see the "orphan" status in process table id "ps -el" */

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
	int pid = fork();
	if(pid == 0) // child process
	{
                printf("\n pid=%d\n", pid);
                printf("+++++++++ Child Created +++++++++++++++++++++++\n");
		printf("I am the child, my Process ID is %d\n", getpid());
		printf("The child's parent process ID is %d\n", getppid());
		sleep(15);
	        printf("file name: [%s] func name = [%s] line num = [%d] pid = %d\n", __FILE__, __func__, __LINE__, pid);
		printf("I am the child, my Process ID is %d\n", getpid());
		printf("The child's parent process ID is %d\n", getppid());
                printf("+++++++++Child Died +++++++++++++++++++++++\n");
	}
	else // parent process
	{       
                printf("\n pid=%d\n", pid);
                printf("+++++++++Parent Start +++++++++++++++++++++++\n");
		sleep(5);
	        printf("file name: [%s] func name = [%s] line num = [%d] pid = %d\n", __FILE__, __func__, __LINE__, pid);
		printf("I am the parent, my Process ID is %d\n", getpid());
		printf("The parent's parent process ID is %d\n", getppid());
                printf("+++++++++Parent Died +++++++++++++++++++++++\n");
	}
		
	return 0;
}
