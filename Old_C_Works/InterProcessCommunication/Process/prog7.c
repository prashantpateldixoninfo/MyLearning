/* Programm create child process after the fork(), and not before that */

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
	printf("This is to demonstrate the fork()\n");
	fork();
	printf("Hello World\n");
	return 0;
}
