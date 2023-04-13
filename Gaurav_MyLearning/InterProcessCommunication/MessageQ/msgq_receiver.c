#include "msgq.h"

int main()
{
	int qid, counter = 1;
	struct 
	{
		long mtype;
		char mtext[SIZE];
	}Message;
	
	printf("I am in Receiver Programme\n");

	/* Accessing the message queue created by sender */
	qid = msgget((key_t) 10, IPC_CREAT|0666);
	printf(" %d\n", qid);
	if(qid == -1)
	{
		perror(" Msgget Error\n");
		exit(-1);
	}
	while(counter != 10)
	{
		/* Reading from message queue */
		msgrcv(qid, &Message, SIZE, counter++, IPC_NOWAIT);
		printf("The message is %s\n", Message.mtext);
		sleep(1);
	}
	return 0;
}
	
