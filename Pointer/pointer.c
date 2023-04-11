#include <stdio.h>

void myfun(int **);

int main()
{
	int k = 6;
	int *ptr = &k;
	printf("address &k = %p\n", &k);
	printf("*ptr = %d\n", *ptr);

	myfun(&ptr);

	printf("*ptr after = %d\n", *ptr);

	return 0;
}

void myfun(int **ptr)
{
	printf("address ptr = %p\n", ptr);
	**ptr = 10;
}
