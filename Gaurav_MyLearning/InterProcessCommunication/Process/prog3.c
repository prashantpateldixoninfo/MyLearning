/* Print the process id of programm */

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
	int pid = getpid();
	printf("Process Id is %d\n", pid);
	return 0;
}
