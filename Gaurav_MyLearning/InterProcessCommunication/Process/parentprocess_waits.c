#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
  #include <sys/types.h>
       #include <sys/wait.h>


int main() {
   int pid;
   int status;
   pid = fork();
   
   // Child process
   if (pid == 0) {
      system("ps -elf");
      sleep(10);
      system("cd ..");
      return 3; //exit status is 3 from child process
   } else {
      sleep(3);
      wait(&status);
      printf("In parent process: exit status from child is decimal %d, hexa %0x\n", status, status);
   }
   return 0;
}
