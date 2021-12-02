#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <time.h>
#include <sys/time.h>

void read_input();

int main() {
    struct timespec begin, end;
    double total = 0;
    for (int i = 0; i < 1; ++i) {
        clock_gettime(CLOCK_REALTIME, &begin);

        const size_t N = 2000;
        int ARRAY[N];

        read_input(ARRAY, N);

        int part1 = 0;
        int part2 = 0;
        for (size_t i = 1; i < N; ++i) {
            if (ARRAY[i] > ARRAY[i - 1])
                ++part1;
        }

        for (size_t i = 3; i < N; ++i) {
            if (ARRAY[i] > ARRAY[i - 3])
                ++part2;
        }

        clock_gettime(CLOCK_REALTIME, &end);
        total += (double)(end.tv_nsec - begin.tv_nsec);
    }

    printf("Time: %lf us\n", (total / 10000) * .001);

    return 0;
}

void read_input(int* ARRAY, size_t N) {
    int fd = open("../inputs/Day01.in", O_RDONLY);
    struct stat input_stat;
    fstat(fd, &input_stat);

    char* mem = (char*) mmap(NULL, input_stat.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
    char* fmem = mem;
    for (size_t i = 0; i < N; ++i) {
        off_t offset = 0;
        char* next;
        ARRAY[i] = strtol(fmem, &next, 10);
        fmem = next+1;
    }

    munmap(mem, input_stat.st_size);
    close(fd);
}
