/* Spawning is fork 'exce' */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(void)
{
	/* If the fork() fails, error will be printed otherwise first either Parent process 
 	* will be executed or Child process whcih in turn calls exec to overlay itself */
	switch(fork())
	{
		case 0:
			printf(" I am Child\n");
			execlp("/bin/ps", "ps", "-al", NULL);
			break;
		case -1:
			perror("Error in fork\n");
			break;
		default:
			printf("This is Parent process\n");
			break;
	}
	return 0;
}
	
