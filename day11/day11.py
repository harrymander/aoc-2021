#!/usr/bin/env python3


import sys

import numpy as np

MIN_FLASH_LEVEL = 10
PRINT_STEPS = 100


def flash_octos(octos, flashed):
    num_flashed = 0

    for irow in range(octos.shape[0]):
        for icol in range(octos.shape[1]):
            has_flashed = flashed[irow][icol]
            energy_level = octos[irow][icol]

            if not has_flashed and energy_level >= MIN_FLASH_LEVEL:
                flashed[irow][icol] = True
                num_flashed += 1

                for i, j in (
                    (irow - 1, icol),
                    (irow + 1, icol),
                    (irow,     icol - 1),
                    (irow,     icol + 1),
                    (irow + 1, icol + 1),
                    (irow - 1, icol + 1),
                    (irow + 1, icol - 1),
                    (irow - 1, icol - 1),
                ):
                    if (i in range(octos.shape[0])
                            and j in range(octos.shape[1])):
                        octos[i][j] += 1

    if num_flashed:
        return num_flashed + flash_octos(octos, flashed)
    else:
        return 0


def step_octos(octos):
    for i in range(octos.shape[0]):
        for j in range(octos.shape[1]):
            octos[i][j] += 1

    flashed = np.zeros((octos.shape[0], octos.shape[1]), dtype=bool)
    num_flashed = flash_octos(octos, flashed)

    for row in range(octos.shape[0]):
        for col in range(octos.shape[1]):
            if flashed[row][col]:
                octos[row][col] = 0

    return num_flashed


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        octos = np.array([
            list(map(int, line.strip())) for line in f.readlines()
        ])

    num_flashed = sum(step_octos(octos) for _ in range(PRINT_STEPS))
    print(num_flashed)

    steps = PRINT_STEPS
    while step_octos(octos) != octos.size:
        steps += 1
    print(steps + 1)
