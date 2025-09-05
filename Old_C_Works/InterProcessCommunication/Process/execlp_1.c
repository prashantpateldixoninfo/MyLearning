/*
 * Running the cat utility via an exec system call
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char *argv[ ])
{
	if (argc > 1) 
	{
    	execlp("/bin/cat", "cat", argv[1], (char *) NULL);
    	perror("exec failure ");
    	return 1;
  	}
  	printf("Usage: %s text_file\n", *argv);
  	return 2;
}

