/* Run the programm in background mode by & and see the process status by command "ps -e" */

#include <stdio.h>
#include<stdlib.h>
int main()
{
	for(long l = 0; l < 40000; l++)
	{
		printf("l is %ld\n", l);
        sleep(5);
	}
	return 0;
}
