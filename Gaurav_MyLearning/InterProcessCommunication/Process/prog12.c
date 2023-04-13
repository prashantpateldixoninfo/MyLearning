/* It will print "Child Process" string, since value return by fork() is always 0 for child process */

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
	int pid = fork();
	if(pid == 0)
	{
		printf("Child Process id=%d\n",pid);
	}
	return 0;
}
