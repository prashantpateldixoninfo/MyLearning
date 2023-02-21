/* Since, child and parent process unable to share their data through varibales. But There is our   way to communicate b/w child and parent process through file sharing */

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/wait.h>

int main()
{
	int fp; //file descriptor
	char chr = 'A';

	int pid = fork();
	if(pid == 0)
	{
		fp = open("baby", O_WRONLY, 0666);
		printf("In child chr is %c\n", chr);
		chr = 'B';
		write(fp, &chr, 1);
		printf("In child chr after change %c\n", chr);
		printf("Child existing\n");
		close(fp);
	}
	else
	{
		wait(0);
		fp = open("baby", O_RDONLY);
		read(fp, &chr, 1);
		printf("chr after parent reads is %c\n", chr);
		close(fp);
	}
		
	return 0;
}
