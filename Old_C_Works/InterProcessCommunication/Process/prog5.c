/* Print the parent process ID of current process */

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
	int pid = getpid();
	int ppid = getppid();
	printf("Process ID is %d\n", pid);
	printf("Parent process ID is %d\n", ppid);
	sleep(15);
	return 0;
}
