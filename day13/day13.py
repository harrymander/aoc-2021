#!/usr/bin/env python3

import sys


def fold_paper(dots, fold):
    axis, number = fold
    new_dots = set()
    for dot in dots:
        if dot[axis] < number:
            new_dots.add(dot)
        else:
            new_pos = 2 * number - dot[axis]
            new_dot = list(dot)
            new_dot[axis] = new_pos
            new_dots.add(tuple(new_dot))
    return new_dots


def print_dots(dots, dotchar='█', nodotchar=' '):
    max_row = max(dot[0] for dot in dots) + 1
    max_col = max(dot[1] for dot in dots) + 1
    for row in range(max_row):
        print(''.join(dotchar if (row, col) in dots else nodotchar
                      for col in range(max_col)))


def main():
    dots = set()
    folds = []
    with open(sys.argv[1]) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            col, row = map(int, line.split(','))
            dots.add((row, col))

        for line in f.readlines():
            fold = line.split()[-1].strip()
            axis, number = fold.split('=')
            folds.append((int(axis == 'x'), int(number)))

    dots = fold_paper(dots, folds[0])
    print(f'After 1 fold there are {len(dots)} dots\n')

    for fold in folds[1:]:
        dots = fold_paper(dots, fold)

    print_dots(dots)


if __name__ == '__main__':
    main()
