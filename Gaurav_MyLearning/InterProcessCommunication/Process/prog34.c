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
    printf("\nAddress of i = %p\n", &i);
    printf("\nPID = %d Line Num: %d\n", getpid(), __LINE__);    
	pid = fork();
	if(pid == 0)
	{
		printf("The intial value of variable 'p' in the child process is %d\n", *p);
		printf("\nPID =%d Line Num: %d\n", getpid(), __LINE__);
		*p=(*p+10);		
        printf("\nAddress of i = %p\n", p);	
		printf("Value of variable 'p' in Child process after incrementation is %d\n", *p);
		printf("Child terminated\n");
	}
	else
	{
		wait((int *)0);
        printf("\nPID = %d Line Num: %d\n", getpid(), __LINE__);    
		printf("value of 'p' in parent process is %d\n", *p);
		printf("Address of parent process is %p\n", p);
	}
	return 0;
}
