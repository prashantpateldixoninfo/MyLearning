/* Here, child process trying to modify the pointer value of 'p'. But parent process doesn't have   modified changes. Siince, every process have own variable */

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>

int main()
{
	int pid=0, i=10;
	int *p = &i; /* local pointer */
	printf("Address of *p = %d\n", *p);
	printf("PID = %d Line Num: [%d]\n", getpid(), __LINE__);
	
	pid = fork();
	if(pid == 0)
	{
		printf("PID = %d Line Num: [%d]\n", getpid(), __LINE__);
		printf("Address of child process is %p\n", p);
		printf("The intial value of variable 'p' in the child process is %d\n", *p);
		*p=20;
		printf("Address of child process is %p\n", &p);
		printf("=====> Child Value of i = %d <======== \n", i);
		printf("Value of variable 'p' in Child process after incrementation is %d\n", *p);
		printf("Child terminated\n");
	}
	else
	{
		printf("PID = %d Line Num: [%d]\n", getpid(), __LINE__);
		wait((int *)0);
		//*p = 30;
		printf("Address of parent process is %p\n", &p);
		printf("value of 'p' in parent process is %d\n", *p);
		printf("=====> Parent Value of i = %d <======== \n", i);
	}
	printf("Before exiting PID = %d Line Num: [%d]\n", getpid(), __LINE__);
	printf("=====> Value of i = %d <======== \n", i);
	return 0;
}
