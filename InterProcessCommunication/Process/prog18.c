/* Sleeping programm will show the status as 'S' in "ps -el" command */

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
	sleep(20);
	printf("The handsome price kissed me\n");
	return 0;
}
