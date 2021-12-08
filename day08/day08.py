#!/usr/bin/env python3

import sys


DIGIT_SEGS = (
    'abcefg',
    'cf',
    'acdeg',
    'acdfg',
    'bcdf',
    'abdfg',
    'abdefg',
    'acf',
    'abcdefg',
    'abcdfg'
)

DIGITS = {tuple(sorted(seg)): i for i, seg in enumerate(DIGIT_SEGS)}


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        unique_patterns, displayed_segments = zip(*(
            tuple(map(str.split, line.split('|'))) for line in f.readlines()
        ))

    unique_lens = tuple(len(s) for s in (DIGIT_SEGS[i] for i in (1, 4, 7, 8)))
    num_unique = 0
    for seg in displayed_segments:
        num_unique += sum(len(s) in unique_lens for s in seg)
    print(num_unique)
