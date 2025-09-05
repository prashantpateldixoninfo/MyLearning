/* Now file "baby1" is opened globally and file contain the string "This is for all the lonely
   people, thinking that life has passed by them". Now child and parent trying to read data 
   from file but they are not closing 'fp'. Due to that it will next buffer from file.
   Here, we'll see that child process moved this shared file handle 10 characters. So when 
   the parent process began to execute, the file handle was on the 11th character */

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
		read(fp, buff, 10);
		buff[10] = '\0';
		printf("Child read : ");
		puts(buff);
		printf("Child existing\n");
	}
	else
	{
		wait(0);
		printf("Parent begins %d\n",getpid());
		read(fp, buff, 10);
		buff[10] = '\0';
		printf("Parent read : ");
		puts(buff);
		printf("Child existing\n");
	}
	return 0;
}
