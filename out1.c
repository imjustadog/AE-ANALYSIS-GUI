#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <math.h>
#include <time.h>
#include <mqueue.h>
#include <string.h>
#include <sys/time.h>


unsigned char buf[128];

int main(void) {
    struct timeval tv;
    struct timezone tz;   
    struct tm *t;
    mqd_t mqd, mqf;
    char timebuf[30];

    time_t ptime;
    unsigned char folder_name[30];
    unsigned char *pfolder = folder_name;
    unsigned char path[60];

    time(&ptime);
    strcpy(folder_name, ctime(&ptime));
    while(*pfolder != '\0') {
        if(*pfolder == '\n') {
            *pfolder = '\0';
            break;
        }
        else if(*pfolder == ' ') 
            *pfolder = '_';
        else if(*pfolder == ':') 
            *pfolder = '-';
        pfolder ++;
    }

    mqd = mq_open("/mqd",O_WRONLY);
    if (mqd < 0) {
        perror("message queue failed to read");
        exit(1);
    }
    mq_send(mqd, folder_name, strlen(folder_name), 0);

    mqf = mq_open("/mqf",O_WRONLY);
    if (mqf < 0){
        perror("message queue failed to read");
        exit(1);
    }

    while (1) {
        printf("test\r\n");
        gettimeofday(&tv, &tz);
        t = localtime(&tv.tv_sec);
        sprintf(timebuf,"%d-%d-%d_%d-%d-%d_%d", 1900+t->tm_year, 1+t->tm_mon, t->tm_mday, t->tm_hour, t->tm_min, t->tm_sec, tv.tv_usec/1000); 

        mq_send(mqf, timebuf, strlen(timebuf), 1);
        sleep(5);
    }
}


