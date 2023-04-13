/* Now let's verify that how the file handle is really shared */

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/wait.h>

int main()
{
	int fp; //file descriptor
	char buff[11];
	fp = open("baby1", O_RDONLY);
	int pid = fork();
	if(pid == 0)
	{
		printf("Child begins %d\n",getpid());
		printf("File handle is %d\n", lseek(fp, 0, 1));
		read(fp, buff, 10);
		buff[10] = '\0';
		printf("Child read : ");
		puts(buff);
		printf("File handle is now %d in the child process\n", lseek(fp, 0, 1));
		printf("Child existing\n");
	}
	else
	{
		wait(0);
		printf("Parent begins %d\n",getpid());
		printf("File handle is %d\n", lseek(fp, 0, 1));
		read(fp, buff, 10);
		buff[10] = '\0';
		printf("Parent read : ");
		puts(buff);
		printf("File handle is now %d in the parent process\n", lseek(fp, 0, 1));
		printf("Child existing\n");
	}
	return 0;
}
