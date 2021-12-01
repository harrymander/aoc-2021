#include <stdio.h>


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

    int current_depth;
    int prev_depth = -1;
    int num_increases = 0;
    while (fscanf(finput, "%d", &current_depth) == 1) {
        if (prev_depth >= 0 && current_depth > prev_depth)
            num_increases++;
        prev_depth = current_depth;
    }

    printf("%d\n", num_increases);
    fclose(finput);
    return 0;
}
