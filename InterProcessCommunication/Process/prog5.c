/* Print the parent process ID of current process */

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
	int ppid = getppid();
	printf("Parent process ID is %d\n", ppid);
	return 0;
}
