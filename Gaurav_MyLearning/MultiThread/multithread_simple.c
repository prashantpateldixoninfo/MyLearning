#include<stdio.h>
#include<stdlib.h>
#include<pthread.h> // pthread
#include<unistd.h>  // sleep()
#include<ctype.h>   // isdigit
#include<limits.h>  // for INT_MAX, INT_MIN

#define NUM_THREADS 4 

/* create thread argument struct for func(int, int) */
typedef struct _thread_data_t
{
    int tid;
    signed int num1;
    signed int num2;
} thread_data_t;


void *addition(void *arg)
{
    thread_data_t *data = (thread_data_t *)arg;
    printf("Thread ID <%d> going to add %d and %d\n", data->tid, data->num1, data->num2);
    sleep(9);
    printf("Addition of %d and %d is %d\n", data->num1, data->num2, data->num1 + data->num2);
}

void *subtraction(void *arg)
{
    thread_data_t *data = (thread_data_t *)arg;
    printf("Thread ID <%d> going to subtract %d and %d\n", data->tid, data->num1, data->num2);
    sleep(5);
    printf("Subtraction of %d and %d is %d\n", data->num1, data->num2, data->num1 - data->num2);
}

void *multipication(void *arg)
{
    thread_data_t *data = (thread_data_t *)arg;
    printf("Thread ID <%d> going to multiply %d and %d\n", data->tid, data->num1, data->num2);
    sleep(7);
    printf("Multipication of %d and %d is %d\n", data->num1, data->num2, data->num1 * data->num2);
}

void *division(void *arg)
{
    thread_data_t *data = (thread_data_t *)arg;
    printf("Thread ID <%d> going to divide %d and %d\n", data->tid, data->num1, data->num2);
    sleep(3);
    if(data->num2 != 0)
    {
    	printf("Division of %d and %d is %f\n", data->num1, data->num2, (float)data->num1/(float)data->num2);
    }
    else
    {
	printf("Unable to divide the number by zero\n");
    }
}

int main(int argc, char *argv[])
{
    void *(*fun_ptr_arr[])(void *) = {addition, subtraction, multipication, division};

    pthread_t thr[NUM_THREADS];
    int rc = 0;

    // create a thread_data_t argument array
    thread_data_t thr_data[NUM_THREADS];

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
    
    // create threads
    for(int i = 0; i < NUM_THREADS; ++i)
    {
        thr_data[i].tid = i;
        thr_data[i].num1 = num11;
	thr_data[i].num2 = num22;

	//fun_ptr_arr[i](&thr_data[i]); // Run as process and comment below thread code
        if((rc = pthread_create(&thr[i], NULL, fun_ptr_arr[i], &thr_data[i])))
	{
            fprintf(stderr, "error: pthread_create, rc: %d\n", rc);
            return EXIT_FAILURE;
        }
    }

    // block until all threads complete
    for(int i = 0; i < NUM_THREADS; ++i)
    {
        pthread_join(thr[i], NULL);
    }
 
    return EXIT_SUCCESS;
}
