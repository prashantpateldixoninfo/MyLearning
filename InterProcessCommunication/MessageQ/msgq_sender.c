#include "msgq.h"

int main()
{
	int qid, counter = 1;
	struct 
	{
		long mtype;
		char mtext[SIZE];
	}Message;

	/* Creating a new message queue */
	qid = msgget((key_t) 10, IPC_CREAT|0666);
	printf(" %d\n", qid);
	if(qid == -1)
	{
		perror(" Msgget Error\n");
		exit(-1);
	}
	strncpy(Message.mtext, "Its My Life \n", SIZE);
	printf("Message sendig ...\n");
	while(counter != 10)
	{
		sprintf(Message.mtext, "I am in %03d ", counter);
		Message.mtype = counter++;
		/* Putting message on the message queue */
		if(msgsnd(qid, &Message, SIZE, 0) == -1)
		{
			perror("msgsnd failed \n");
			exit(-2);
		}
	}
	return 0;
}
