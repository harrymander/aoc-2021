#!/usr/bin/env python3

import itertools
from math import inf
import sys


def print_visited(visited):
    for row in visited:
        print(''.join(str(int(i)) for i in row))


def print_distances(distances):
    for row in distances:
        print(' '.join(f'{i:02}' if i < inf else '??' for i in row))


def main():
    with open(sys.argv[1]) as f:
        cavern = [list(map(int, line.strip())) for line in f.readlines()]

    rows, cols = len(cavern), len(cavern[0])
    distances = [[inf] * cols for _ in range(rows)]
    distances[0][0] = 0
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
                new_distance = distances[row][col] + cavern[to_row][to_col]
                if new_distance < distances[to_row][to_col]:
                    distances[to_row][to_col] = new_distance

        loc = min(unvisited, key=lambda l: distances[l[0]][l[1]])

    print(distances[rows - 1][cols - 1])


if __name__ == '__main__':
    main()
