PROGS = streamread out1
CXX = gcc
CFLAGS += -Wall
LDLIBS += -lrt -pthread -lm
OBJS = $(PROGS).o

all: $(PROGS)

%: %.o
	$(CXX) $(LDLIBS) $(CFLAGS) $^ -o $@


%.o: %.c
	$(CXX) -c $(LDLIBS) $(CFLAGS) $^ -o $@

clean:
	rm -f *.o $(PROGS)



