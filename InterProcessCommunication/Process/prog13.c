/* If fork() becomes unsuccessful then it return -1 */

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
	int pid = fork();
	if(pid < 0)
	{
		printf("Fork failed\n");
	}
	else
	{
		printf("Fork succeeded\n");
	}
	return 0;
}
