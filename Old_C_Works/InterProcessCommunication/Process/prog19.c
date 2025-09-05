/* Programm is running in infinite loop and process status will be showing as 
   'R' */

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
	for(;;);	
	return 0;
}
