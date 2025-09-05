/* Create the multiple Child process from parent process i.e. current process.
   It will create total 8 processes. i.e. 2 the power of 3 = 8 */

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
	fork();
	fork();
	fork();
	printf("Hello World\n");
	return 0;
}
