#include "shm_sem.h"

FILE * fptr = NULL;

int main()
{
    int start = 1;
    void * shm = NULL;
    struct sh_dat * sh_ptr;
    int shmid, semid;

    shmid = shmget((key_t) 1234, sizeof(struct sh_dat), 0666 | IPC_CREAT);
    if(shmid == -1)
    {
        print_flog("Shared Memory creation failed");
        exit(EXIT_FAILURE);
    }
    print_flog("Shared Memory created");

    semid = semget((key_t) 1235, 1, 0666 | IPC_CREAT);
    if(semid == -1)
    {
        print_flog("Semaphore creation failed");
        shmctl(shmid, IPC_RMID, NULL);
        exit(EXIT_FAILURE);
    }
    print_flog("Semaphore created");

    if(semctl(semid, 0, GETVAL, 1) == 0) // Semaphore value not yet set
    {
        // Initially making the semaphore available
        if(semctl(semid, 0, SETVAL, 1) == -1)
        {
            print_flog("Semaphore SETVAL failed");
            shmctl(shmid, IPC_RMID, 0);
            semctl(semid, IPC_RMID, 0);
            exit(EXIT_FAILURE);
        }
        print_flog("Semaphore SETVAL Succeed");
    }

    // Attaching the shared memory to server process
    shm = shmat(shmid, (void *)0, 0);
    if(shm == (void *) - 1)
    {
        print_flog("Shared Memory attach failed");
        shmctl(shmid, IPC_RMID, NULL);
        semctl(semid, IPC_RMID, 0);
        exit(EXIT_FAILURE);
    }
    print_flog("Shared Memory Attached");

    sh_ptr = (struct sh_dat *)shm;
    while(start) // entering the loop
    {
        sleep(2);
        // Waiting while client write data
        if(semaphore_p(semid)) // Check if client has written the data
        {
            // Black[30], Red[31], Green[32], Yellow[33], Blue[34], Purple[35], Cyan[36], White[37]
            mycolor(genRandoms(30, 37)); // Random color setting
            printf("You wrote: %s\n", sh_ptr -> text);
            colorreset(); // Color reseting
            print_flog("Message received from client: %s", sh_ptr -> text);
            semaphore_v(semid); // Giving it to client after reading the data
            if(strncmp(sh_ptr -> text, "end", 3) == 0)
            {
                start = 0; // Stopping the program
                print_flog("Message received from client: %s", sh_ptr -> text);
            }
        }
    }

    // Detaching the shared memory
    if(shmdt(sh_ptr) == -1)
    {
        print_flog("Shared Memory Detachment Failed");
        exit(EXIT_FAILURE);
    }
    print_flog("Shared Memory Detachment Succeed");
    if(shmctl(shmid, IPC_RMID, 0) == -1)
    {
        print_flog("Shared Memory Removal Failed");
        exit(EXIT_FAILURE);
    }
    print_flog("Shared Memory Removal Succeed");
    if(semctl(semid, IPC_RMID, 0) == -1)
    {
        print_flog("Semaphonre Removal Failed");
        fprintf(stderr, "semctl(IPC_RMID) failed\n");
        exit(EXIT_FAILURE);
    }
    print_flog("Semaphonre Removal Succeed");
    exit(EXIT_SUCCESS);
}
