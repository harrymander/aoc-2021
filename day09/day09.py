#!/usr/bin/env python3

import itertools
import math
import sys


def find_basin_size(heights, visited_locations, row, col):
    num_visited = 1
    visited_locations[row][col] = True
    adjacent = ((row - 1, col),
                (row + 1, col),
                (row, col - 1),
                (row, col + 1))

    height = heights[row][col]
    for neighbor_row, neighbour_col in adjacent:
        visited = visited_locations[neighbor_row][neighbour_col]
        neighbour_height = heights[neighbor_row][neighbour_col]
        if not visited and height <= neighbour_height:
            num_visited += find_basin_size(
                heights, visited_locations,
                neighbor_row, neighbour_col
            )

    return num_visited


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        heights = [[int(i) for i in line.strip()] for line in f.readlines()]

    rows, cols = len(heights), len(heights[0])

    for row in heights:
        row.insert(0, 10)
        row.append(10)
    heights.insert(0, [10] * (cols + 2))
    heights.append([10] * (cols + 2))

    risk_level_total = 0
    low_points = []
    for row, col in itertools.product(range(1, rows + 1), range(1, cols + 1)):
        height = heights[row][col]
        if (height < heights[row - 1][col]
                and height < heights[row + 1][col]
                and height < heights[row][col - 1]
                and height < heights[row][col + 1]):
            low_points.append((row, col))
            risk_level_total += height + 1

    print(risk_level_total)

    visited_locations = [[i >= 9 for i in row] for row in heights]
    basin_sizes = []
    for row, col in low_points:
        basin_size = find_basin_size(heights, visited_locations,
                                     row, col)
        basin_sizes.append(basin_size)

    print(math.prod(sorted(basin_sizes)[-3:]))
