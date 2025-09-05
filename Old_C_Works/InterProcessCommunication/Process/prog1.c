/* Print the command line argumets */

#include <stdio.h>

int main(int argc, char *argv[])
{
	for(int i = 0; i < argc; i++)
	{
		printf("Argumets are %s\n", argv[i]);

	}
	return 0;
}

