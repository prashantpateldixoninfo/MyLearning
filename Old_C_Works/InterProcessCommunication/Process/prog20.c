/* First programm will run is sleeping mode and then in infinite loop.
   Run the programm in background and see the process status through 
   "ps -el" command */

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
	printf("Run the ps -el command\n");
	sleep(20);
	printf("Run the ps -el command once more\n");
	for(;;);
	return 0;
}
