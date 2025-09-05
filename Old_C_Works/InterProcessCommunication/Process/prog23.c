/* Due to inconsistency in prevoius programm output. We can use process 
   synchronization through "wait(0)" API */

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>

int main()
{
	printf("Ready to fork\n");
	int pid = fork();
	if(pid == 0) // child process
	{
		printf("Child starts\n");
		for(int i = 0; i < 500000; i++)
			printf("%d\t", i);
		printf("child ends\n");
	}
	else if(pid > 0) //parent process
	{
		printf("Parent starts\n");
		wait(0);
		for(int j = 0; j < 500000; j++)
			printf("%d....", j);
		printf("Parents ends\n");
	}
	return 0;
}
