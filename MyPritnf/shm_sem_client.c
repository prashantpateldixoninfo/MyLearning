#include "shm_sem.h"

FILE *fptr = NULL;

int main()
{
	int start = 1;
	void *shm = NULL;
	struct sh_dat *sh_ptr;
	char buffer[TEXT_SZ];
	int shmid, semid;

    fptr = fopen("mylog.txt", "a+");

	shmid = shmget((key_t)1234, sizeof(struct sh_dat), 0666 | IPC_CREAT);
	if(shmid == -1)
	{
		fprintf(fptr, "[%s] [%s] [%s] [%d] shmget failed\n", timestamp(), __FILE__, __func__, __LINE__);
		exit(EXIT_FAILURE);
	}
    sleep(1);
	fprintf(fptr, "[%s] [%s] [%s] [%d] Shared Memory created\033[0m\n", timestamp(), __FILE__, __func__, __LINE__);
	
	semid = semget((key_t)1235, 1, 0666 | IPC_CREAT);
	if(semid == -1)
	{
		fprintf(fptr, "[%s] [%s] [%s] [%d] semget failed\n", timestamp(), __FILE__, __func__, __LINE__);
		shmctl(shmid, IPC_RMID, NULL);
		exit(EXIT_FAILURE);
	}
    sleep(1);
	fprintf(fptr, "[%s] [%s] [%s] [%d] Semaphore created\n", timestamp(), __FILE__, __func__, __LINE__);

	shm = shmat(shmid, (void *)0, 0);
	if(shm == (void *)-1)
	{
		fprintf(fptr, "[%s] [%s] [%s] [%d] shmat failed\n", timestamp(), __FILE__, __func__, __LINE__);
		exit(EXIT_FAILURE);
	}
    sleep(1);
	fprintf(fptr, "[%s] [%s] [%s] [%d] Shared Memory Attached\n", timestamp(), __FILE__, __func__, __LINE__);
	sh_ptr = (struct sh_dat *)shm;
	while(start) 				/* entering the loop */
	{
		/* Waiting while server reads the data written by the client */
		if(semaphore_p(semid))	/* Check if server has written the data */
		{
            // Black[30], Red[31], Green[32], Yellow[33], Blue[34], Purple[35], Cyan[36], White[37]
            mycolor(genRandoms(30, 37));
			printf("Enter some text: ");
            colorreset();
			fprintf(fptr, "[%s] [%s] [%s] [%d] Enter some text: ", timestamp(), __FILE__, __func__, __LINE__);
			fgets(buffer, TEXT_SZ, stdin);
		
			strncpy(sh_ptr->text, buffer, TEXT_SZ);
			fprintf(fptr, "[%s] [%s] [%s] [%d] User has type the message: %s", timestamp(), __FILE__, __func__, __LINE__, buffer);
			semaphore_v(semid);	/* Giving the memory to the server for reading */
			sleep(1);
			if(strncmp(sh_ptr->text, "end",3) == 0)
			{
				start = 0;		/* Stopping the program */
			    fprintf(fptr, "[%s] [%s] [%s] [%d] User has type the message: %s", timestamp(), __FILE__, __func__, __LINE__, sh_ptr->text);
			}
		}
	}
	if(shmdt(sh_ptr) == -1)
	{
		fprintf(fptr, "[%s] [%s] [%s] [%d] shmdt failed\n", timestamp(), __FILE__, __func__, __LINE__);
		exit(EXIT_FAILURE);
	}
	fprintf(fptr, "[%s] [%s] [%s] [%d] Shared Memory Detached\n", timestamp(), __FILE__, __func__, __LINE__);
	exit(EXIT_SUCCESS);
}

