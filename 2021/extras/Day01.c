#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <time.h>
#include <sys/time.h>

void read_input();

int main(int argc, char** argv) {
    if (argc < 2) {
        puts("Usage: ./Day01 <num_runs>");
        return -1;
    }
    struct timespec begin, end;
    long double avg = 0;
    for (int i = 0; i < strtol(argv[1], NULL, 10); ++i) {
        if (clock_gettime(CLOCK_REALTIME, &begin) == -1) {
            perror("start time error");
        }

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


        if (clock_gettime(CLOCK_REALTIME, &end) == -1) {
            puts("Usage: ./Day01 <num_runs>");
            return -1;
        }

        long double ns = (long double)(end.tv_nsec - begin.tv_nsec) / 1000000000L;
        long double sec = (long double) end.tv_sec - begin.tv_sec;
        long double t = ns + sec;
        avg += (t - avg) / (i + 1);
    }

    printf("Time: %Lf us\n", avg * 1000000);

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
