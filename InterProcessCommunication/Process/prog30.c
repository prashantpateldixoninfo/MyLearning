/* Below programm would generate "core dump" */

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
	int i=0,j=0;
	i = 10/j;
	printf("Value of i is %d\n", i);
	return 0;
}
