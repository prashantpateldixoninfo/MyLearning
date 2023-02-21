/* This is program for Shell using the EXCL command */

#include <stdio.h>
#include <malloc.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(void)
{
	char *arr[12];
	char *input = NULL;
	int i = 0;
	input = (char *)malloc(sizeof(char) * 12);
	printf("#SHELL:>");
	fgets(input, 32, stdin);
	input[strlen(input) - 1] = '\0';
	arr[0] = input;
	while(*(++input) != '\0')
	{
		if(*input == '\0')
		{
			*input = '\0';
			arr[++i] = ++input;
		}
	}
	arr[++i] = NULL;
	execvp(arr[0], arr);
}
