/* Create the Child process from parent process i.e. current process */

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{   int pid=getpid();
    printf("\nProcessid of cureent process=%d\n", pid);
	fork();
	printf("Hello World\n");
        sleep(10);
	return 0;
}
