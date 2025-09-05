/* Print the process ID and put the programm in background state and see the status of programm by command "ps -e" */

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
	printf("Process ID is %d\n", getpid());
	for(long i = 0; i < 400000; i++)
	{
		printf("i is %ld\n", i);
	}
	return 0;
}
