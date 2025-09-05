#include <time.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

FILE *fptr = NULL;

#define print_log(fmt, ...) printf("[%s] [%s] [%s] [%d] ", timestamp(), __FILE__, __func__, __LINE__), printf((fmt), ##__VA_ARGS__), printf("\n")

#define print_flog(fmt, ...) fprintf(fptr, "[%s] [%s] [%s] [%d] ", timestamp(), __FILE__, __func__, __LINE__), fprintf(fptr, (fmt), ##__VA_ARGS__), fprintf(fptr, "\n")


char * timestamp(){
    time_t now = time(NULL);
    char * time = asctime(gmtime(&now));
    time[strlen(time)-1] = '\0';    // Remove \n
    return time;
}

int exe_cmd_read_from_file()
{
    FILE *ls_cmd = popen("find . -type f -name 'a*.txt' | grep -o -E '[0-9]+' | sort -rn | head -n 1", "r");
    if (ls_cmd == NULL)
    {
        fprintf(stderr, "popen(3) error");
        exit(EXIT_FAILURE);
    }

    static char buff[1024];
    size_t n;
    while ((n = fread(buff, 1, sizeof(buff)-1, ls_cmd)) > 0)
    {
        buff[n] = '\0';
        printf("file_content is = %s", buff);
    }

    if (pclose(ls_cmd) < 0)
        perror("pclose(3) error");

    return 0;
}

int main(int argc, char* argv[])
{
    fptr = fopen("mylog_time.txt", "a+"); 
    print_log("Hello");
    print_log("%s %d", "Dixon", 2023);
    print_flog("%s %d", "Prashant", 1980);
    fclose(fptr);
    exe_cmd_read_from_file();
    return 0;
}
