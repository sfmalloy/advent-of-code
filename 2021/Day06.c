#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

typedef unsigned long long u64;

const size_t FILE_BUFFER = 1024;

void init_fish(u64* fish);

u64 make_fish(int num_runs, u64* fish);

int main() {
    u64 fish[9];
    init_fish(fish);
    struct timespec start, finish;
    clock_gettime(CLOCK_REALTIME, &start);

    u64 part1 = make_fish(80, fish);
    u64 part2 = make_fish(176, fish);

    clock_gettime(CLOCK_REALTIME, &finish);

    printf("%llu\n%llu\n", part1, part2);
    printf("Time: %.3lf µs\n", (double)((finish.tv_sec - start.tv_sec) + ((finish.tv_nsec - start.tv_nsec) / 1e9)) * 1e6);

    return 0;
}

void init_fish(u64* fish) {
    for (size_t i = 0; i < 9; ++i) {
        fish[i] = 0;
    }

    FILE* file = fopen("inputs/Day06.in", "r");
    char input[FILE_BUFFER];
    fscanf(file, "%s", input);

    char* token = strtok(input, ",");
    while (token != NULL) {
        ++fish[strtoul(token, NULL, 10)];
        token = strtok(NULL, ",");
    }

    fclose(file);
}

u64 make_fish(int num_runs, u64* curr_fish) {
    u64 new_fish[9];
    for (int k = 0; k < num_runs; ++k) {
        new_fish[0] = curr_fish[1];
        new_fish[1] = curr_fish[2];
        new_fish[2] = curr_fish[3];
        new_fish[3] = curr_fish[4];
        new_fish[4] = curr_fish[5];
        new_fish[5] = curr_fish[6];
        new_fish[6] = curr_fish[7] + curr_fish[0];
        new_fish[7] = curr_fish[8];
        new_fish[8] = curr_fish[0];
        for (size_t i = 0; i < 9; ++i) {
            curr_fish[i] = new_fish[i];
        }
    }

    u64 total = 0;
    for (size_t i = 0; i <= 8; ++i) {
        total += curr_fish[i];
    }

    return total;
}
