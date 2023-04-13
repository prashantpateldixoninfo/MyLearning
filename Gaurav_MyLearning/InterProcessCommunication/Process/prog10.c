/* It will create child process and print the parent and child process id */

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
	fork();
	printf("The PID is %d\n PPID is %d\n", getpid(), getppid());
    sleep(10);
      
	return 0;
}
