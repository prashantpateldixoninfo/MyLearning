#include<stdio.h>
#include<unistd.h>
#include<sys/wait.h>
#include<stdlib.h>

int main()
{
   int pid;
   int status;
   pid = fork();
   
   if (pid == 0) // Child process
   {
      system("ps -elf");
      sleep(10);
      //system("ps -elf");
	  system("man wait");
	  //int a = 5/0;
      return 3; //exit status is 3 from child process
   } 
   else 
   { 
	  // Parent
      sleep(3);
      wait(&status);
      printf("In parent process: exit status from child is decimal %d, hexa %0x\n", status, status);
   }
   return 0;
}
