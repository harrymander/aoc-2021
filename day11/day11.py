#!/usr/bin/env python3


import itertools
import sys

import numpy as np

MIN_FLASH_LEVEL = 10
PRINT_STEPS = 100


def flash_octos(octos, flashed):
    num_flashed = 0
    rows, cols = octos.shape
    for irow, icol in itertools.product(range(rows), range(cols)):
        if not flashed[irow][icol] and octos[irow][icol] >= MIN_FLASH_LEVEL:
            flashed[irow][icol] = True
            num_flashed += 1
            octos[max(0, irow - 1):min(rows, irow + 2),
                  max(0, icol - 1):min(cols, icol + 2)] += 1

    if num_flashed:
        return num_flashed + flash_octos(octos, flashed)
    else:
        return 0


def step_octos(octos):
    octos += 1
    flashed = np.zeros((octos.shape[0], octos.shape[1]), dtype=bool)
    num_flashed = flash_octos(octos, flashed)
    octos[flashed] = 0
    return num_flashed


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        octos = np.array([
            list(map(int, line.strip())) for line in f.readlines()
        ])

    num_flashed = sum(step_octos(octos) for _ in range(PRINT_STEPS))
    print(f'Number of flashes after {PRINT_STEPS} steps:', num_flashed)

    steps = PRINT_STEPS
    while step_octos(octos) != octos.size:
        steps += 1
    print('All flashed simultaneously on step', steps + 1)
