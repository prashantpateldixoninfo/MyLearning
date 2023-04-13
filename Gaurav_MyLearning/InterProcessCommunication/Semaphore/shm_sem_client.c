
#include "shm_sem.h"

int semaphore_p(int sem_id);
int semaphore_v(int sem_id);

int main()
{
	int start = 1;
	void *shm = NULL;
	struct sh_dat *sh_ptr;
	char buffer[TEXT_SZ];
	int shmid, semid;

	shmid = shmget((key_t)1234, sizeof(struct sh_dat), 0666 | IPC_CREAT);
	if(shmid == -1)
	{
		fprintf(stderr, "shmget failed\n");
		exit(EXIT_FAILURE);
	}
	
	semid = semget((key_t)1235, 1, 0666 | IPC_CREAT);
	if(semid == -1)
	{
		fprintf(stderr, "semget failed\n");
		shmctl(shmid, IPC_RMID, NULL);
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
		if(semaphore_p(semid))	/* Check if server has written the data */
		{
			printf("Enter some text: ");
			fgets(buffer, TEXT_SZ, stdin);
		
			strncpy(sh_ptr->text, buffer, TEXT_SZ);
			semaphore_v(semid);	/* Giving the memory to the server for reading */
			sleep(1);
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
	exit(EXIT_SUCCESS);
}

int semaphore_p(int sem_id)
{
	struct sembuf sem_b;
	sem_b.sem_num = 0;
	sem_b.sem_op = -1;
	sem_b.sem_flg = SEM_UNDO;
	if(semop(sem_id, &sem_b, 1) == -1)
	{
		fprintf(stderr, "semaphore_p failed \n");
		return 0;
	}
	return 1;
}

int semaphore_v(int sem_id)
{
	struct sembuf sem_b;
	sem_b.sem_num = 0;
	sem_b.sem_op = 1;
	sem_b.sem_flg = SEM_UNDO;
	if(semop(sem_id, &sem_b, 1) == -1)
	{
		fprintf(stderr, "semaphore_v failed \n");
		return 0;
	}
	return 1;
}
