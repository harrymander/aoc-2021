#!/usr/bin/env python3


import re
import sys


def main():
    with open(sys.argv[1]) as f:
        match = re.match(
            r'target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)',
            f.readline())
    box = (int(match[1]), int(match[2])), (int(match[3]), int(match[4]))

    v0_y = abs(box[1][0]) - 1
    max_height = int((v0_y) * (v0_y + 1) / 2)
    print(max_height)


if __name__ == '__main__':
    main()
