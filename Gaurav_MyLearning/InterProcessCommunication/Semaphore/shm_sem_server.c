#include "shm_sem.h"

int semaphore_p(int sem_id);
int semaphore_v(int sem_id);

int main()
{
	int start = 1;
	void *shm = NULL;
	struct sh_dat *sh_ptr;
	int shmid, semid;

	/* Creating the semaphore and shared memory */
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
	
	/* Initially making the semaphore available */
	if(semctl(semid, 0, SETVAL, 1) == -1)
	{
		fprintf(stderr, "semctl(SETVAL) failed\n");
		shmctl(shmid, IPC_RMID, NULL);
		shmctl(semid, IPC_RMID, NULL);
		exit(EXIT_FAILURE);
	}
	
	/* Attaching the shared memory to server process */
	shm = shmat(shmid, (void *)0, 0);
	if(shm == (void *)-1)
	{
		fprintf(stderr, "shmat failed\n");
		exit(EXIT_FAILURE);
	}
	sh_ptr = (struct sh_dat *)shm;
	while(start) 				/* entering the loop */
	{
		sleep(2);
		if(semaphore_p(semid))	/* Check if client has written the data */
		{
			printf("You wrote: %s", sh_ptr->text);
			semaphore_v(semid);	/* Giving it to client after reading the data */
			if(strncmp(sh_ptr->text, "end",3) == 0)
			{
				start = 0;		/* Stopping the program */
			}
		}
	}

	/* Detaching the shared memory */
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
	if(shmctl(semid, IPC_RMID, 0) == -1)
	{
		fprintf(stderr, "semctl(IPC_RMID) failed\n");
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
