#!/usr/bin/env python3

import sys


def calc_rating(nums, most_common):
    if len(nums) == 1:
        return nums[0]

    ones = [num[1:] for num in nums if num[0]]
    zeros = [num[1:] for num in nums if not num[0]]

    if (num_ones := len(ones)) > (num_zeros := len(zeros)):
        next_num = 1
    elif num_ones < num_zeros:
        next_num = 0
    else:
        next_num = 1

    if not most_common:
        next_num = int(not next_num)

    keep = ones if next_num else zeros
    return [next_num] + calc_rating(keep, most_common)


def bin_list_to_int(n):
    return int(''.join(map(str, n)), 2)


if __name__ == '__main__':
    filename = sys.argv[1]

    with open(filename) as f:
        lines = []
        for line in f.readlines():
            lines.append(list(map(int, line.strip())))

    one_counts = lines[0].copy()
    for line in lines[1:]:
        for i, d in enumerate(line):
            one_counts[i] += d

    num_lines = len(lines)
    num_bits = len(one_counts)

    gamma = int(
        ''.join('1' if b >= num_lines // 2 else '0' for b in one_counts), 2
    )
    epsilon = (2**num_bits - 1) ^ gamma

    power_consumption = gamma * epsilon
    print(f'{gamma=} * {epsilon=} = {power_consumption}')

    o2_gen_rating = bin_list_to_int(calc_rating(lines, True))
    co2_scrubber_rating = bin_list_to_int(calc_rating(lines, False))

    life_support_rating = o2_gen_rating * co2_scrubber_rating
    print(f'{o2_gen_rating=} * {co2_scrubber_rating=} = {life_support_rating}')
