#include <time.h>
#include <stdio.h>
#include <stdlib.h>

extern void solve();

int main() {
    struct timespec begin, end;
    long double avg = 0;
    for (int i = 0; i < 1000; ++i) {
        if (clock_gettime(CLOCK_REALTIME, &begin) == -1) {
            puts("start time error");
            return -1;
        }

        solve();

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
