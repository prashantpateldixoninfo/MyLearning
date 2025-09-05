#include <stdio.h>
#include <stdarg.h>

void variadic_funct(int count, ...)
{
	va_list args;
	va_start(args, count);
	printf("variadic : argument count = %d\n", count);
	for(int i = 0; i < count; i++)
	{
		printf("argument %d = %d, ", i + 1, va_arg(args, int));
	}
	printf("\n");
	vprintf("My ARGS = %d %d %d\n", args);
	va_end(args);
}

#define MY_INPUT 10, 20, 30

int main(int argc, char *argv[])
{

	variadic_funct(3, MY_INPUT);
	return 0;
}
