/* This is a server program which creates a fifo and writes into it */

/* Procedure to create FIFO through command line
 *		"/etc/mknode fdFifo1 p" where mknode is command, fdFifo1 is FIFO name and p is for 
 *		permission.
 * To Display the content of FIFO
 * 		cat fdFifo1
 */
 

#include "fifo.h"

int main()
{
	int fd;
	printf("I am in Server\n");

	/* Creating a new fifo */
	mkfifo(Fifo1, 0777);

	/* Opening the filo for writing */
	fd = open(Fifo1, O_WRONLY, 0777);

	/* Writing to the file */
	write(fd, "Its my life", 15);
	
	/* Close the fifo */
	close(fd);
	return 0;
}
