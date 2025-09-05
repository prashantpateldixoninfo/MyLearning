#include<stdio.h>
#include<ctype.h>
#include<stdlib.h>
#include<unistd.h>
#include<pthread.h>

struct my_thread_data
{
    int num1;
    int num2;
};

void *mysum(void * data)
{
    printf("mysum is called\n");
    struct my_thread_data *m_data = (struct my_thread_data *)data;
    printf("Addition of %d and %d is %d\n", m_data->num1, m_data->num2,  m_data->num1 +  m_data->num2);
}

int main(int argc, char *argv[])
{
    if(argc < 3 || argc > 3)
    {
	printf("Usage: ./<exe_name> <num1> <num2>\n");
        return EXIT_FAILURE;
    }

    int num11 = atoi(argv[1]); // In fail case it return 0
    if(num11 == 0 && !isdigit(*argv[1]))
    {
        printf("Error: <num1> is not integer\n");
        return EXIT_FAILURE;
    }
    
    int num22 = atoi(argv[2]); // In fail case it return 0
    if(num22 == 0 && !isdigit(*argv[2]))
    {
        printf("Error: <num2> is not integer\n");
        return EXIT_FAILURE;
    }

    //mysum(num11, num22);
    pthread_t thread_id;
    printf("Before Thread File name: [%s] Func Name: [%s] Line Num: [%d]\n", __FILE__, __func__, __LINE__);

    struct my_thread_data my_data;
    my_data.num1 = num11;
    my_data.num2 = num22;
    pthread_create(&thread_id, NULL, mysum, &my_data); 
    pthread_join(thread_id, NULL);
    printf("Main After Thread\n");

    return 0;
}
