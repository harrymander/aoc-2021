#!/usr/bin/env python3

import itertools
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

SEGMENTS = 'abcdefg'
NUM_SEGMENTS = len(SEGMENTS)


def decode_digit(segs, order='abcdefg'):
    reordered_segs = sorted(SEGMENTS[order.index(s)] for s in segs)
    try:
        return DIGIT_SEGS.index(''.join(reordered_segs))
    except ValueError:
        return -1


def check_order(segments, order):
    digits = [-1]
    for segment in segments:
        digit = decode_digit(segment, order)
        if digit in digits:
            return False
    return True


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        all_segments, all_sensor_segments = zip(*(
            map(str.split, line.split('|'))
            for line in f.readlines()
        ))

    unique_lens = tuple(len(s) for s in (DIGIT_SEGS[i] for i in (1, 4, 7, 8)))
    num_unique_len_digits = 0
    for seg in all_sensor_segments:
        num_unique_len_digits += sum(len(s) in unique_lens for s in seg)
    print('Number of digits with unique number of segments:',
          num_unique_len_digits)

    total = 0
    for segments, sensor_segments in zip(all_segments, all_sensor_segments):
        for order in itertools.permutations(SEGMENTS, NUM_SEGMENTS):
            if check_order(segments, order):
                total += sum(10**i * decode_digit(seg, order) for
                             i, seg in enumerate(reversed(sensor_segments)))

    print('Sum of all sensor outputs', total)
