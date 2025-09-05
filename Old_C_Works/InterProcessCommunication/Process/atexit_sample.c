#include <stdio.h>
#include <stdlib.h>

static int abc = 5;

void myexitfunc() {
   printf("My Called cleanup function - %s %d\n", __func__, ++abc);
   return;
}

void exitfunc() {
   printf("I am in exitfunc\n");
   atexit(myexitfunc);
   printf("Called cleanup function - %s %d\n", __func__, ++abc);
   return;
}

int main() {
   atexit(exitfunc);
   printf("Hello, World! %d\n", ++abc);
   exit (0);
   printf("After exit(0)\n");
}	
