#!/usr/bin/env python3

import sys

import numpy as np


def fold_paper(paper, fold):
    axis, number = fold

    if axis:  # axis == 'x'
        fold1, fold2 = paper[:, :number], paper[:, number + 1:]
    else:
        fold1, fold2 = paper[:number, :], paper[number + 1:, :]

    fold2 = np.flip(fold2, axis)
    return fold1 | fold2


if __name__ == '__main__':
    max_x, max_y = 0, 0
    dots = []
    folds = []
    with open(sys.argv[1]) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            x, y = map(int, line.split(','))
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
            dots.append((x, y))

        for line in f.readlines():
            fold = line.split()[-1].strip()
            axis, number = fold.split('=')
            folds.append((int(axis == 'x'), int(number)))

    paper = np.zeros((max_y + 1, max_x + 1), dtype=bool)
    for x, y in dots:
        paper[y, x] = True

    paper = fold_paper(paper, folds[0])
    print(f'After 1 fold there are {paper.sum()} dots\n')

    for fold in folds[1:]:
        paper = fold_paper(paper, fold)

    for row in paper:
        print(''.join('#' if dot else ' ' for dot in row))
