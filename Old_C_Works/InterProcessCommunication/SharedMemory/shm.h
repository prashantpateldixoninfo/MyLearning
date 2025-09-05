#ifndef _SHM_H_
#define _SHM_H_

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>

#define TEXT_SZ 32

struct sh_dat
{
	int available;
	char text[TEXT_SZ];
};
#endif
