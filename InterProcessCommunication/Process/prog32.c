/* Let see how many active process can be created by fork() */

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdlib.h>

int main()
{
	int pid=0, i=1;
	for(;;)
	{
		pid = fork();
		if(pid < 0)
			printf("Maximum concurrent process are %d\n", i);
		if(pid == 0)
			i++;
		else
		{
			wait(0);
			exit(0);
		}
	}
	return 0;
}
