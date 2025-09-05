/* Filename: sigHandlerSigAction.c */
#include<stdio.h>
#include<unistd.h>
#include<signal.h>

void handleSignals(int signum);

int main(void) {
   void (*sigHandlerReturn)(int);
   struct sigaction mysigaction;
   mysigaction.sa_handler = handleSignals;
   sigemptyset(&mysigaction.sa_mask);
   mysigaction.sa_flags = 0;
   sigaction(SIGINT, &mysigaction, NULL);
   
   if (mysigaction.sa_handler == SIG_ERR) {
      perror("signal error: ");
      return 1;
   }
   mysigaction.sa_handler = handleSignals;
   sigemptyset(&mysigaction.sa_mask);
   mysigaction.sa_flags = 0;
   sigaction(SIGQUIT, &mysigaction, NULL);
   
   if (mysigaction.sa_handler == SIG_ERR) {
      perror("signal error: ");
      return 1;
   }
   while (-1) {
      printf("\nTo terminate this program, perform either of the following: \n");
      printf("1. Open another terminal and issue command: kill %d\n", getpid());
      printf("2. Issue CTRL+C 2 times (second time it terminates)\n");
      sleep(10);
   }
   return 0;
}

void handleSignals(int signum) {
   switch(signum) {
      case SIGINT:
      printf("\nYou have entered CTRL+C \n");
      printf("Now reverting SIGINT signal to perform default action\n");
      signal(SIGINT, SIG_DFL);
      break;
      case SIGQUIT:
      printf("\nYou have entered CTRL+\\ \n");
      break;
      default:
      printf("\nReceived signal number %d\n", signum);
      break;
   }
   return;
}
