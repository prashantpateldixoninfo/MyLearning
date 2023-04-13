#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

int main()
{
	alarm(5);
	for(;;);
	return 0;
}
