/* Both parent and child process is trying to write the data simulataneously
   which result in weired output. */

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
	int pid = fork();
	if(pid == 0) // child process
	{
		for(int i = 0; i < 500000; i++)
			printf("%d\t", i);
	}
	else if(pid > 0) //parent process
	{
		for(int j = 0; j < 500000; j++)
			printf("%d....", j);
	}
	return 0;
}
