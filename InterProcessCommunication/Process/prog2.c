/* Run the programm in background mode by & and see the process status by command "ps -e" */

#include <stdio.h>

int main()
{
	for(long l = 0; l < 40000; l++)
	{
		printf("l is %ld\n", l);
	}
	return 0;
}
