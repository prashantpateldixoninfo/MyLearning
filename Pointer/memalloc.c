#include <stdio.h>
#include <stdlib.h>
  
void memallocate(int num, int **ptr);

int main()
{
  
    // This pointer will hold the
    // base address of the block created
    int* ptr;
    int n, i;
  
    // Get the number of elements for the array
    printf("Enter number of elements:");
    scanf("%d",&n);
    printf("Entered number of elements: %d\n", n);
  
  	memallocate(n, &ptr);

    // Print the elements of the array
    printf("The elements of the array are: ");
    for (i = 0; i < n; ++i) {
    	printf("%d, ", ptr[i]);
    }
	printf("\n");
  
    return 0;
}

void memallocate(int num, int **ptr)
{
    // Dynamically allocate memory using malloc()
    *ptr = (int* )malloc(num * sizeof(int));
  
    // Check if the memory has been successfully
    // allocated by malloc or not
    if (*ptr == NULL) {
        printf("Memory not allocated.\n");
        exit(0);
    }
    else {
  		// Memory has been successfully allocated
        printf("Memory successfully allocated using malloc.\n");
  
        // Get the elements of the array
        for (int i = 0; i < num; ++i) {
            *(*ptr+i) = i + 1;
        }
    }
}
