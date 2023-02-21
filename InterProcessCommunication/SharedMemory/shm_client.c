
#include "shm.h"

int main()
{
	int start = 1;
	void *shm = NULL;
	struct sh_dat *sh_ptr;
	char buffer[TEXT_SZ];
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
	while(start) 				/* entering the loop */
	{
		/* Waiting while server reads the data written by the client */
		if(sh_ptr->available == 1)	/* Check if server has written the data */
		{
			sleep(2);
			printf("waiting for server to read...\n");
		}
		printf("Enter some text: ");
		fgets(buffer, TEXT_SZ, stdin);
		
		strncpy(sh_ptr->text, buffer, TEXT_SZ);
		sh_ptr->available = 1;	/* Giving the memory to the server for reading */
		if(strncmp(sh_ptr->text, "end",3) == 0)
		{
			start = 0;		/* Stopping the program */
		}
	}
	if(shmdt(sh_ptr) == -1)
	{
		fprintf(stderr, "shmdt failed\n");
		exit(EXIT_FAILURE);
	}
	exit(EXIT_SUCCESS);
}
