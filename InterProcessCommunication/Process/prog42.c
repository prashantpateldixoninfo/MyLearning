#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>

int main()
{
	FILE *fp;
	char buff[11];
	int pid, i;
	fp = fopen("book", "w+");

	for(i=0; i<1024; i++)
		fprintf(fp, "A");
	for(i=0; i<1024; i++)
		fprintf(fp, "B");
	for(i=0; i<1024; i++)
		fprintf(fp, "C");
	for(i=0; i<1024; i++)
		fprintf(fp, "D");

	fclose(fp);
	
	fp = fopen("book", "r");
    pid = fork();

	if(pid == 0)
	{
		fread(buff, sizeof(buff), 1, fp);
		buff[10] = '\0';
		printf("After child read file pointer ftell-> %d %s\n", ftell(fp), buff);
		sleep(5);
		printf("In child after parent read file pointer ftell-> %d %s\n", ftell(fp), buff);
		fread(buff, sizeof(buff), 1, fp);
		buff[10]='\0';
		printf("After child 2nd time read file pointer %d %s\n", ftell(fp), buff);
	}
	else
	{
		sleep(1);
		printf("intially in parent file poiter %d %s\n", ftell(fp), buff);
		fread(buff, sizeof(buff), 1, fp);
		buff[10]='\0';
		printf("After Parent read file pointer %d %s\n", ftell(fp), buff);
	}
	return 0;
}
