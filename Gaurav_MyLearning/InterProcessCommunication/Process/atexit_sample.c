
   #include <stdio.h>
#include <stdlib.h>

void exitfunc() {
   printf("Called cleanup function - exitfunc()\n");
   return;
}

int main() {
   atexit(exitfunc);
   int i=1;
   printf("Hello, World!\n");
   if (i==1)
   {
   atexit(exitfunc);
   printf("\n Gaurav Pandey in block\n");
   }
   printf("\nGaurav pandey outside the block");

   exit (0);
} 
