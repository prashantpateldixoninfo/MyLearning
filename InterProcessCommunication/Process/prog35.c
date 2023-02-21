/* Here, child process trying to modify the value of 'i' which is global. 
   But parent process doesn't have these changes. Siince, every process have own variable */

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>

int i=10; // global variable

int main()
{
	int pid=0;

	pid = fork();
	if(pid == 0)
	{
		printf("The intial value of variable i in the child process is %d\n",i);
		i+=10;		
		printf("Value of variable i in Child process after incrementation is %d\n", i);
		printf("Child terminated\n");
	}
	else
	{
		wait(0);
		printf("value of i in parent process is %d\n", i);
	}
	return 0;
}
