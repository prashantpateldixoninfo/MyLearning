/* Here, child process trying to modify the value of 'i'. But parent process doesn't have these 
   changes. Siince, every process have own variable */

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>

int main()
{
	int pid=0, i=10, j=50;
	pid = fork();
	if(pid == 0)
	  {sleep(15);
		printf("The intial value of variable i in the child process is %d\n",i);
		i+=10;		
		printf("Value of variable i in Child process after incrementation is %d\n", i);
		printf("Child terminated\n");
	}
	else
	{i=30;
     j=100;  
		
	printf("value of i in paren process is %d\n", i);
    wait(0);
	}
    printf("\nmain i=%d main j=%d\n", i, j);
	return 0;
}
