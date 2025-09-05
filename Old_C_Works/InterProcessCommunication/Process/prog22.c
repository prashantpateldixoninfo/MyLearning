/* Parent process will wait untill child process is terminated from process
   table */

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
		sleep(10);
		for(int i = 0; i < 5000; i++)
			printf("%d\t", i);
		printf("child ends\n");
	}
	else if(pid > 0) //parent process
	{
		wait(0);
		printf("Parents Process\n");
	}
	return 0;
}
