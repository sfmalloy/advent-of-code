#include <stdlib.h>
#include <stdio.h>
#include <string.h>

typedef unsigned long long u64;
const size_t FILE_BUFFER = 1024;
void init_fish(u64 fish[]);

int main() {
    u64 curr_fish[9];
    init_fish(curr_fish);

    u64 new_fish[9];
    u64 part1 = 0;
    for (int k = 0; k < 256; ++k) {
        new_fish[0] = curr_fish[1];
        new_fish[1] = curr_fish[2];
        new_fish[2] = curr_fish[3];
        new_fish[3] = curr_fish[4];
        new_fish[4] = curr_fish[5];
        new_fish[5] = curr_fish[6];
        new_fish[6] = curr_fish[7] + curr_fish[0];
        new_fish[7] = curr_fish[8];
        new_fish[8] = curr_fish[0];
        for (size_t i = 0; i <= 8; ++i) {
            curr_fish[i] = new_fish[i];
        }

        if (k == 80) {
            for (size_t i = 0; i <= 8; ++i) {
                part1 += curr_fish[i];
            }
        }
    }

    u64 part2 = 0;
    for (size_t i = 0; i <= 8; ++i) {
        part2 += curr_fish[i];
    }
    printf("%llu\n", part1);
    printf("%llu\n", part2);

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
}
