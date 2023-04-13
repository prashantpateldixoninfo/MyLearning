#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

void abc(int signo)
{
	printf("Received Signal with signo %d\n", signo);
	exit(0);
}

int main()
{
	int i=0, j=50;
	signal(SIGFPE, abc); // key, function
	//signal(SIGFPE, SIG_DFL); // key, function
	j=j/i;
	return 0;
}
