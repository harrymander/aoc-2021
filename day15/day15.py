#!/usr/bin/env python3

import itertools
from math import inf
import sys


def find_least_risky_path_score(cavern):
    rows, cols = len(cavern), len(cavern[0])
    risks = [[inf] * cols for _ in range(rows)]
    risks[0][0] = 0
    loc = (0, 0)

    unvisited = set(itertools.product(range(rows), range(cols)))
    while loc != (rows - 1, cols - 1):
        row, col = loc
        unvisited.remove(loc)

        neighbours = []
        if row - 1 > 0:
            neighbours.append((row - 1, col))
        if row + 1 < rows:
            neighbours.append((row + 1, col))
        if col - 1 > 0:
            neighbours.append((row, col - 1))
        if col + 1 < cols:
            neighbours.append((row, col + 1))

        for to_loc in neighbours:
            if to_loc in unvisited:
                to_row, to_col = to_loc
                new_risk = risks[row][col] + cavern[to_row][to_col]
                if new_risk < risks[to_row][to_col]:
                    risks[to_row][to_col] = new_risk

        loc = min(unvisited, key=lambda l: risks[l[0]][l[1]])

    return risks[rows - 1][cols - 1]


def main():
    with open(sys.argv[1]) as f:
        small_cavern = [list(map(int, line.strip())) for line in f.readlines()]

    print(find_least_risky_path_score(small_cavern))

    wide_cavern = []
    for row in small_cavern:
        new_row = row.copy()
        for extra in range(4):
            new_row.extend([((i + extra + 1) % 9) or 9 for i in row])
        wide_cavern.append(new_row)

    cavern = wide_cavern.copy()
    for extra in range(4):
        for row in wide_cavern:
            cavern.append([((i + extra + 1) % 9) or 9 for i in row])

    print(find_least_risky_path_score(cavern))


if __name__ == '__main__':
    main()
