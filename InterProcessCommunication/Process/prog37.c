/* Here, child and parent process variable having same address. Although, duplicate copy of
   varaible is defined for each process(chald, parent) and kept in swap area. But while execution
   of process put in main area. therefore, these variable have same address value. */

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>

int main()
{
	int i=10, pid=0;
	printf("Before fork i is %d\n", i);
	pid = fork();
	if(pid == 0)
	{
		printf("in child i's address is %p\n", &i);
		i = 20;
		printf("i is %d\n", i);
	}
	else
	{
		sleep(1);
		printf("In Parent i's address is %p\n", &i);
		printf("i is %d\n", i);
	}
	return 0;
}
