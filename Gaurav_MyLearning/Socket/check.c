#include <sys/types.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <stdio.h>

int main()
{
    printf("MSG_CONFIRM = %d\n", MSG_CONFIRM);
    printf("MSG_DONTROUTE = %d\n", MSG_DONTROUTE);
    printf("MSG_DONTWAIT = %d\n", MSG_DONTWAIT);
    printf("MSG_EOR = %d\n", MSG_EOR);
    printf("MSG_MORE = %d\n", MSG_MORE);
    printf(" MSG_NOSIGNAL = %d\n",  MSG_NOSIGNAL);
    printf("MSG_OOB = %d\n",  MSG_OOB);
    return 0;
}

