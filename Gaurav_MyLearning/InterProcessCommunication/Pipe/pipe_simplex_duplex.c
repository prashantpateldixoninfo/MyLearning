/* This program demonstrates PIPE in both a SIMPLE and DUPLEX mode depending in the
 * flag specified during the compiler 
 * 		
 * 		1	If NO flag are specified during the compilation. This will work as normal 
 * 			Simplex mode and
 * 		2	If -DFULL is specified during compilation the this program will work in a 
 * 			FULL DUPLEX mode.(g++ -DFULL -o pipe_simplex_duplex pipe_simplex_duplex.c)
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define SIZE 20

typedef struct 
{
	int Id;
	char Name[SIZE];
	float Salary;
}Employee;

int main()
{
	int fd01[2];
	Employee e01, e11;
#ifdef FULL
	int fd02[2];
	Employee e02, e22;
#endif

	e01.Id = 001;
	strcpy(e01.Name, "Prashant");
	e01.Salary	= 123.45;
#ifdef FULL
	e02.Id = 002;
    strcpy(e02.Name, "Anand");
    e02.Salary  = 456.12;
#endif

	pipe(fd01);
#ifdef FULL
	pipe(fd02);
#endif

	switch(fork())
	{
		case 0: // child process
			close(fd01[1]); // close the child's write
		#ifdef FULL
            close(fd02[0]); // close the child's read
            write(fd02[1], &e02, sizeof(e02)); // e02 writes to e22
		#endif
			read(fd01[0], &e11, sizeof(e11)); // e11 reads from e01
			
			printf("Child process->Read from Parent Process\n");
			printf("Id is:\t%d\n", e11.Id);
			printf("Name is:\t%s\n", e11.Name);
			printf("Salary is:\t%f\n", e11.Salary);
			printf("-------------------------\n");
			break;
		default: // Parent process
			close(fd01[0]); // close the parent's read 
		#ifdef FULL
            close(fd02[1]); // close the parent's write
            read(fd02[0], &e22, sizeof(e22)); // e22 reads from e02
		#endif
			write(fd01[1], &e01, sizeof(e01)); // e01 writes to e11

		#ifdef FULL	
			printf("Parent process->Write to Child Process \n");
			printf("Id is:\t%d\n", e22.Id);
			printf("Name is:\t%s\n", e22.Name);
			printf("Salary is:\t%f\n", e22.Salary);
		#endif
			printf("-------------------------\n");
			break;
	}
	return 0;
}
