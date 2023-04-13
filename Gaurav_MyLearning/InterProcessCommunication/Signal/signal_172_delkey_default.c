#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

int main()
{
	printf("Press DEL key to terminate\n");
	signal(SIGINT, SIG_DFL);
	for(;;);
	return 0;
}
