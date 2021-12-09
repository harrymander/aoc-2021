#!/usr/bin/env python3

import sys


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        smoke_map = [[int(i) for i in line.strip()] for line in f.readlines()]

    rows, cols = len(smoke_map), len(smoke_map[0])

    smoke_map_expanded = smoke_map.copy()
    for row in smoke_map_expanded:
        row.insert(0, 10)
        row.append(10)
    smoke_map_expanded.insert(0, [10] * (cols + 2))
    smoke_map_expanded.append([10] * (cols + 2))

    risk_level_total = 0
    for row in range(1, rows + 1):
        for col in range(1, cols + 1):
            height = smoke_map_expanded[row][col]
            if (height < smoke_map_expanded[row - 1][col]
                    and height < smoke_map_expanded[row + 1][col]
                    and height < smoke_map_expanded[row][col - 1]
                    and height < smoke_map_expanded[row][col + 1]):
                risk_level_total += height + 1

    print(risk_level_total)
