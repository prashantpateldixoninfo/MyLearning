/* It will print the parent process id, since value return by fork() for child process will be 0 */

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
	int pid = fork();
	if(pid > 0)
	{
		printf("Parent Process ID is %d\n", pid);
	}
	return 0;
}
