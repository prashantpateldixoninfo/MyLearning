
/* This is a client program which opens a fifo already created by server and read from it
*/

#include "fifo.h"

int main()
{
	int fd;
	char str[15];	
	printf("I am in Client\n");

	/* Opens the filo created by server*/
	fd = open(Fifo1, O_RDONLY, 0777);

	/* Reading from the file */
	read(fd, str, 15);
	
	/* Close the fifo */
	close(fd);

	printf("I read \" %s \" string from the server\n", str);
	unlink(Fifo1);
	return 0;
}
