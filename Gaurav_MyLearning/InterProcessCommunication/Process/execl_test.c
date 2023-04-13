#include<stdio.h>
#include<unistd.h>

void main() {
   printf("pid =%d and ppid= %d filename: [%s] function Name: [%s] line num: [%d]\n", getpid(), getppid(), __FILE__, __func__, __LINE__);
   printf("\n excelfile in execution\n");
   sleep(10);
   execl("./helloworld", "./helloworld", (char *)0);
   printf("This wouldn't print\n");
   
return;
}

