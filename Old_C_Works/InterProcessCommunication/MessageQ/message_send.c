#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <stdio.h>
#include <string.h>

#define MSGSZ     128


/*
 *  * Declare the message structure.
*/

typedef struct mybuf 
{
	long    mtype;
    char    mtext[MSGSZ];
} message_buf;

main(int argc, char *argv[])
{
    int msqid;
    int msgflg = IPC_CREAT | 0666;
    key_t key;
    message_buf sbuf;
    size_t buf_length;

/*
* Get the message queue id for the
* name" 1234, which was created by
* the server.
*/

	key = 1234;

	(void) fprintf(stderr, "\nmsgget: Calling msgget(%d,%o)\n",key, msgflg);
	
	if ((msqid = msgget(key, msgflg )) < 0) 
	{
		perror("msgget");
    	return -1;
	}
	else 
	{
		printf("msqid = %d\n", msqid);
		(void) fprintf(stderr,"msgget: msgget succeeded: msqid = %d\n", msqid);
	}
/*
 * We'll send message type 1
*/


	sbuf.mtype = 1;
    
    (void) fprintf(stderr,"msgget: msgget succeeded: msqid = %d\n", msqid);
    
	if( argv[1] != NULL)
	{
    	(void) strcpy(sbuf.mtext, argv[1]);
    }
	else
	{
		(void) strcpy(sbuf.mtext, "Please enter some message\n");
	}
    (void) fprintf(stderr,"msgget: msgget succeeded: msqid = %d\n", msqid);
    
    buf_length = strlen(sbuf.mtext) + 1 ;

/*
 * Send a message.
*/
	if (msgsnd(msqid, &sbuf, buf_length, IPC_NOWAIT) < 0) 
	{
       printf ("%d, %d, %s, %d\n", msqid, sbuf.mtype, sbuf.mtext, buf_length);
        perror("msgsnd");
        return -1;
	}
	else 
	{
      	printf("Message: \"%s\" Sent\n", sbuf.mtext);
	} 
    return 1;
}












