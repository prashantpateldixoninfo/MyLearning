/* Let explore that how wait() API is working. If int variable is passed in 
   wait() and higher 8 bits are updated but lower 8 bits initialized with 0,
   then programm terminated normally. But if passed int value have lower 8 bits 
   updated and higher 8 bits intialize to 0, then programm terminated abnormally
   */
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdlib.h>

int main()
{
	int i=0, pid=0, exitstat=0, status=0;
	pid = fork();
	if(pid == 0)
	{
		printf("enter exit status:");
		scanf("%d", &i);
		exit(i);
	}
	else
	{
		wait(&status);
		if(status & 0xff != 0) // lower bits
		{
			printf("Signal Interrupted\n");
		}
		else
		{
			exitstat = (int) status/256; // divide to conver higher 8 bits to lower 8 bits
			printf("Exit status from %d was %d \n", pid, exitstat);
		}
	}
	return 0;
}
