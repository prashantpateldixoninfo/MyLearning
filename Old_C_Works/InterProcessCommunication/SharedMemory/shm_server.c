#include "shm.h"

int main()
{
	int start = 1;
	void *shm = NULL;
	struct sh_dat *sh_ptr;
	int shmid;

	shmid = shmget((key_t)1234, sizeof(struct sh_dat), 0666 | IPC_CREAT);
	if(shmid == -1)
	{
		fprintf(stderr, "shmget failed\n");
		exit(EXIT_FAILURE);
	}
	shm = shmat(shmid, (void *)0, 0);
	if(shm == (void *)-1)
	{
		fprintf(stderr, "shmat failed\n");
		exit(EXIT_FAILURE);
	}
	sh_ptr = (struct sh_dat *)shm;
	sh_ptr->available = 0; 		/* Making it non available i.e. currently being written by client */
	while(start) 				/* entering the loop */
	{
		if(sh_ptr->available)	/* Check if client has written the data */
		{
			printf("You wrote: %s", sh_ptr->text);
			sleep(2);
			sh_ptr->available = 0;	/* Giving it to client after reading the data */
			if(strncmp(sh_ptr->text, "end",3) == 0)
			{
				start = 0;		/* Stopping the program */
			}
		}
	}
	if(shmdt(sh_ptr) == -1)
	{
		fprintf(stderr, "shmdt failed\n");
		exit(EXIT_FAILURE);
	}
	if(shmctl(shmid, IPC_RMID, 0) == -1)
	{
		fprintf(stderr, "shmctl(IPC_RMID) failed\n");
		exit(EXIT_FAILURE);
	}
	exit(EXIT_SUCCESS);
}
	
