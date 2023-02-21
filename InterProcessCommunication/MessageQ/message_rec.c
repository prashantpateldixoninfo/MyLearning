#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <stdio.h>

#define MSGSZ     128


/*
* Declare the message structure.
*/

typedef struct mybuf {
    long    mtype;
    char    mtext[MSGSZ];
} message_buf;

main()
{
    int msqid;
    key_t key;
    message_buf  rbuf;

	/*
    * Get the message queue id for the
 	* "name" 1234, which was created by
    * the server.
	*/

	key = 1234;

    if ((msqid = msgget(key, 0666)) < 0) {
        perror("msgget");
        return -1;
    }
	/*
    * Receive an answer of message type 1.
    */

	if (msgrcv(msqid, &rbuf, MSGSZ, 1, 0) < 0) {
        perror("msgrcv");
        return -1;
    }
	printf("msqid = %d\n", msqid);

	/*
    * Print the answer.
    */
	
	printf("%s\n", rbuf.mtext);
    return 0;
}






