/* Create the multiple Child process from parent process i.e. current process.
   It will create total 4 process, i.e. 1 parent, 2 child, and 1 grandson */

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
	fork();
	fork();
	printf("Hello World\n");
	return 0;
}
