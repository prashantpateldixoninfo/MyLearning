#ifndef _SHM_H_
#define _SHM_H_

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <time.h>

#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/sem.h>

#define TEXT_SZ 32

struct sh_dat
{
	char text[TEXT_SZ];
};

char * timestamp();
void mycolor(int color);
void colorreset();
int genRandoms(int lower, int upper);
int semaphore_p(int sem_id);
int semaphore_v(int sem_id);

#endif
