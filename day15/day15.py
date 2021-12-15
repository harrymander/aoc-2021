#!/usr/bin/env python3

from heapq import heappop, heappush
from math import inf
import sys


def find_least_risky_path_score(cavern):
    """
    Dijkstra's algorithm
    """

    rows, cols = len(cavern), len(cavern[0])
    risks = [[inf] * cols for _ in range(rows)]
    risks[0][0] = 0
    loc = (0, 0)

    queue = [(0, loc)]
    visited = set()
    while True:
        current_risk, loc = heappop(queue)
        if loc == (rows - 1, cols - 1):
            return current_risk

        row, col = loc
        visited.add(loc)

        neighbours = []
        if row - 1 > 0:
            neighbours.append((row - 1, col))
        if row + 1 < rows:
            neighbours.append((row + 1, col))
        if col - 1 > 0:
            neighbours.append((row, col - 1))
        if col + 1 < cols:
            neighbours.append((row, col + 1))

        for to_loc in (n for n in neighbours if n not in visited):
            to_row, to_col = to_loc
            new_risk = current_risk + cavern[to_row][to_col]
            if new_risk < risks[to_row][to_col]:
                risks[to_row][to_col] = new_risk
                heappush(queue, (new_risk, to_loc))


def main():
    with open(sys.argv[1]) as f:
        small_cavern = [list(map(int, line.strip())) for line in f.readlines()]

    print(find_least_risky_path_score(small_cavern))

    cavern = [row.copy() for row in small_cavern]
    for row, original_row in zip(cavern, small_cavern):
        for extra in range(1, 5):
            row.extend([(i + extra) % 9 or 9 for i in original_row])

    rows = cavern.copy()
    for extra in range(1, 5):
        for row in rows:
            cavern.append([(i + extra) % 9 or 9 for i in row])

    print(find_least_risky_path_score(cavern))


if __name__ == '__main__':
    main()
