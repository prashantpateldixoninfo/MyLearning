#include "shm_sem.h"

FILE * fptr = NULL;

int main()
{
    int start = 1;
    void * shm = NULL;
    struct sh_dat * sh_ptr;
    char buffer[TEXT_SZ];
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
        // Waiting while server reads the data written by the client
        if(semaphore_p(semid)) // Check if server has written the data
        {
            // Black[30], Red[31], Green[32], Yellow[33], Blue[34], Purple[35], Cyan[36], White[37]
            mycolor(genRandoms(30, 37)); // Random color setting
            printf("Enter some text: ");
            colorreset(); // Color reseting
            print_flog("Enter some text: ");

            fgets(buffer, TEXT_SZ, stdin); // Read from keyboard into buffer
            buffer[strlen(buffer) - 1] = '\0'; // Removed \n from buffer
            strncpy(sh_ptr -> text, buffer, TEXT_SZ); // Copy buffer into shared memory(sh_ptr->text)

            print_flog("User has type the message: %s", buffer);
            semaphore_v(semid); // Giving the memory to the server for reading
            sleep(1);
            if(strncmp(sh_ptr -> text, "end", 3) == 0)
            {
                start = 0; // Stopping the program
                print_flog("User has type the message: %s", sh_ptr -> text);
            }
        }
    }

    if(shmdt(sh_ptr) == -1)
    {
        print_flog("Shared Memory detached failed");
        shmctl(shmid, IPC_RMID, NULL);
        semctl(semid, IPC_RMID, 0);
        exit(EXIT_FAILURE);
    }
    print_flog("Shared Memory Detached");

    shmctl(shmid, IPC_RMID, NULL);
    semctl(semid, IPC_RMID, 0);
    exit(EXIT_SUCCESS);
}
