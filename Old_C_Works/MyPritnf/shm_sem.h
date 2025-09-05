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

extern FILE * fptr;

struct sh_dat
{
    char text[TEXT_SZ];
};

#define print_flog(fmt, ...) \
    fptr = fopen("mylog.txt", "a+"); \
    fprintf(fptr, "[%s] [%s] [%s] [%d] ", timestamp(), __FILE__, __func__, __LINE__), fprintf(fptr, (fmt), ##__VA_ARGS__), fprintf(fptr, "\n"); \
    fclose(fptr);

char * timestamp();
void mycolor(int color);
void colorreset();
int genRandoms(int lower, int upper);
int semaphore_p(int sem_id);
int semaphore_v(int sem_id);

#endif
