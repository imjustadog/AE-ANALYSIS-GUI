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

int main(void) {
    struct timeval tv;
    struct timezone tz;   
    struct tm *t;
	
    mqd_t mqd;
    char sendbuf[100];

    mqd = mq_open("/mq1",O_WRONLY);
    if (mqd < 0) {
        printf("%s\r\n",strerror(errno));
	return -1;
    }

    while(1) {
        printf("test\r\n");

        gettimeofday(&tv, &tz);
        t = localtime(&tv.tv_sec);
        sprintf(sendbuf,"%d-%d-%d_%d-%d-%d_%d", 1900+t->tm_year, 1+t->tm_mon, t->tm_mday, t->tm_hour, t->tm_min, t->tm_sec, tv.tv_usec/1000);
        mq_send(mqd, sendbuf, strlen(sendbuf), 1);

        sleep(2);
    }
}


