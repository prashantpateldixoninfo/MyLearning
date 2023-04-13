#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

void abc(int signo)
{
	printf("Time to wake up my friend\n");
	//sleep(5);
}

int main()
{
	signal(SIGALRM, abc);
	alarm(5);
	pause();
	//for(;;);
	return 0;
}
