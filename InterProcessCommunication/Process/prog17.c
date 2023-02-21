/* What happaned if parent child process terminate before parent procese.
   This phenomena called as "Zombei Process" */

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
	if(fork() > 0)
	{
		printf("Parent Process\n");
		sleep(10);
	}
		
	return 0;
}
