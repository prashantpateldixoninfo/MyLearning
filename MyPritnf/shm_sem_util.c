#include "shm_sem.h"

extern FILE *fptr;

char * timestamp()
{
    time_t ltime; // calendar time
    ltime = time(NULL); // get current cal time 

    char * curr_local_time = asctime(localtime(&ltime));
    curr_local_time[strlen(curr_local_time) - 1] = '\0'; // removed \n
    return curr_local_time;
}
void mycolor(int color)
{
    printf("\033[1;%dm", color);
}

void colorreset()
{
    printf("\033[0m");
}

int genRandoms(int lower, int upper)
{
    // Use current time as seed for random generator
    srand(time(0));
    int num = (rand() % (upper - lower + 1)) + lower;
    return num;
}

int semaphore_p(int sem_id)
{
	struct sembuf sem_b;
	sem_b.sem_num = 0;
	sem_b.sem_op = -1;
	sem_b.sem_flg = SEM_UNDO;
	if(semop(sem_id, &sem_b, 1) == -1)
	{
		fprintf(fptr, "[%s] [%s] [%s] [%d] semaphore_p failed \n", timestamp(), __FILE__, __func__, __LINE__);
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
		fprintf(fptr, "[%s] [%s] [%s] [%d] semaphore_v failed \n", timestamp(), __FILE__, __func__, __LINE__);
		return 0;
	}
	return 1;
}
