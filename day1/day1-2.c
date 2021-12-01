#include <stdio.h>


#define WINDOW_SIZE 3


int main(const int argc, const char *argv[])
{
    const char *filename = argv[1];
    if (!filename) {
        printf("Usage: %s [input]\n", argv[0]);
        return 1;
    }

    FILE *finput = fopen(filename, "r");
    if (!finput) {
        perror("Cannot open file");
        return 1;
    }

    int window_sums[WINDOW_SIZE] = {0};
    int prev_window_sum = -1;

    int num_increases = 0;
    int i = 0;
    int iwindow = 0;
    int depth;

    while (fscanf(finput, "%d", &depth) == 1) {
        for (int j = 0; j < (i < WINDOW_SIZE ? i + 1 : WINDOW_SIZE); j++)
            window_sums[j] += depth;

        i++;

        if (i > WINDOW_SIZE - 1) {
            const int window_sum = window_sums[iwindow];
            window_sums[iwindow] = 0;

            if (prev_window_sum >= 0 && window_sum > prev_window_sum)
                num_increases++;
            prev_window_sum = window_sum;

            iwindow = (iwindow + 1) % WINDOW_SIZE;
        }
    }

    printf("%d\n", num_increases);
    fclose(finput);
    return 0;
}
