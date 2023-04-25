#include <time.h>
#include <stdio.h>
#include <string.h>

FILE *fptr = NULL;

#define print_log(fmt, ...) printf("[%s] [%s] [%s] [%d] ", timestamp(), __FILE__, __func__, __LINE__), printf((fmt), ##__VA_ARGS__), printf("\n")

#define print_flog(fmt, ...) fprintf(fptr, "[%s] [%s] [%s] [%d] ", timestamp(), __FILE__, __func__, __LINE__), fprintf(fptr, (fmt), ##__VA_ARGS__), fprintf(fptr, "\n")


char * timestamp(){
    time_t now = time(NULL);
    char * time = asctime(gmtime(&now));
    time[strlen(time)-1] = '\0';    // Remove \n
    return time;
}

int main(int argc, char* argv[])
{
    fptr = fopen("mylog_time.txt", "a+"); 
    print_log("Hello");
    print_log("%s %d", "Dixon", 2023);
    print_flog("%s %d", "Prashant", 1980);
    fclose(fptr);

    return 0;
}
