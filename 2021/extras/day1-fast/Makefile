CC := gcc
CFLAGS := -m64 -no-pie

a.out: Day01.o Driver.o
	gcc $(CFLAGS) $^ -o $@

Day01.o: Day01.s

Drive.o: Driver.c

clean:
	$(RM) a.out *.o
