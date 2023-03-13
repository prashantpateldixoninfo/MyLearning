#include<stdio.h>
#include<sys/types.h>
#include<unistd.h>

void main() {
   printf("getpid = %d getppid = %d File name: [%s] Funct Name: [%s] Line Num: [%d]\n", getpid(), getppid(), __FILE__, __func__, __LINE__);
   execl("./helloworld", "./helloworld", (char *)0);
   printf("This wouldn't print File name = [%s]\n", __FILE__);
   return;
}
