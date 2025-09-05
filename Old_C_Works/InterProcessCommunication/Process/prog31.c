/* Once core dupm is generated, the 7th bit of a temporary 2 byte variable that
   is put ON to reflect a core dump or zonmbie */

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>

int main()
{
	int i=0, pid=0, exitstat=0, status=0, j=0;
	pid = fork();
	if(pid == 0) // child process
	{
		i = 10/j; // core dump will generate
	}
	else
	{
		wait(&status);
		if(status & 0x80)
			printf("our core dump\n");
	}
	return 0;
}
