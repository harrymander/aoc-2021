#!/usr/bin/env python3


import re
import sys


def shoot(v0, box):
    x, y = 0, 0
    vx, vy = v0

    while True:
        x += vx
        y += vy

        vy -= 1
        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1

        if x > box[0][1] or y < box[1][0]:
            return False
        if all(b[0] <= p <= b[1] for p, b in zip((x, y), box)):
            return True


def main():
    with open(sys.argv[1]) as f:
        match = re.match(
            r'target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)',
            f.readline())
    box = (int(match[1]), int(match[2])), (int(match[3]), int(match[4]))

    v0_y = abs(box[1][0]) - 1
    max_height = int((v0_y) * (v0_y + 1) / 2)
    print('Highest possible y position:', max_height)

    num_starting_velocities = 0
    for vx in range(1, box[0][1] + 1):
        for vy in range(box[1][0], v0_y + 1):
            num_starting_velocities += int(shoot((vx, vy), box))
    print('Number of different starting velocities:', num_starting_velocities)


if __name__ == '__main__':
    main()
