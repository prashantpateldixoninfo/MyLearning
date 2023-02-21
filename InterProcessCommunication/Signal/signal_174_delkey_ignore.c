#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

int main()
{
	printf("Press DEL<ctrl + c> key\n");
	signal(SIGINT, SIG_IGN);
	for(;;);
	return 0;
}
