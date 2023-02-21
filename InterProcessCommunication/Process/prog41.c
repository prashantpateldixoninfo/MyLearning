/* Now we will use high level file function for previous programm.
   Since, the fread() function in the child process reads 1024 bytes by
   default, when the parent process is given the time-slice, the file
   pointer is at the end of file. As a result, nothing is displayed on screen.*/

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/wait.h>

int main()
{
	FILE *fp; //file descriptor
	char buff[11];
	fp = fopen("baby1", "r");
	int pid = fork();
	if(pid == 0)
	{
		printf("Child begins %d\n",getpid());
		printf("Intial Child file pointer %d\n", ftell(fp));
		fread(buff, sizeof(buff), 1, fp);
		buff[10] = '\0';
		printf("Child read : ");
		puts(buff);
		printf("After child process reads data from file the file pointer is %d\n", ftell(fp));
		printf("Child existing\n");
	}
	else
	{
		wait(0);
		printf("Parent begins %d\n",getpid());
		printf("Intial Parent file pointer %d\n", ftell(fp));
		fread(buff, sizeof(buff), 1, fp);
		buff[10] = '\0';
		printf("Parent read : ");
		puts(buff);
		printf("After parent process reads data from file the file pointer is %d\n", ftell(fp));
		printf("Parent existing\n");
	}
	return 0;
}
