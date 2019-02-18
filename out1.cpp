#include <iostream>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <mqueue.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <sys/time.h>
#include <stdio.h>

using namespace std;

int main(void) {
    struct timeval tv;
    struct timezone tz;   
    struct tm *t;

    pid_t pid;	
    mqd_t mqd;
    struct mq_attr setattr;
    unsigned int prio;
    int recvlen;
    char sendbuf[100];

    setattr.mq_maxmsg = 10;
    setattr.mq_msgsize = 10; 

    while(1) {
        cout << "test" << endl;

        mqd = mq_open("/mq1",O_WRONLY);
        if (mqd < 0) {
            cout << strerror(errno) << endl;
	    return -1;
        }

        gettimeofday(&tv, &tz);
        t = localtime(&tv.tv_sec);
        sprintf(sendbuf,"%d-%d-%d %d-%d-%d %d", 1900+t->tm_year, 1+t->tm_mon, t->tm_mday, t->tm_hour, t->tm_min, t->tm_sec, tv.tv_usec/1000);
        mq_send(mqd, sendbuf, strlen(sendbuf), 0); //数值越大，优先级越大，0为最小优先级
        mq_close(mqd);
        sleep(2);
    }
}


