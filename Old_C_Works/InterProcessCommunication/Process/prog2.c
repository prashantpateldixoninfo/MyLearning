/* Run the programm in background mode by & and see the process status by command "ps -e" */

#include <stdio.h>
#include <unistd.h>

int main()
{
    sleep(10);
    for(long l = 0; l < 400000; l++)
    {
        printf("l is %ld\n", l);
    }
    return 0;
}
