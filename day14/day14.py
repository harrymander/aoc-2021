#!/usr/bin/env python3

import operator
import sys


def grow_polymer(pair_counts, char_counts, rules):
    new_counts = {}
    for pair, count in filter(operator.itemgetter(1), pair_counts.items()):
        pair_counts[pair] = 0
        insert = rules[pair]
        for new_pair in (pair[0] + insert, insert + pair[1]):
            new_counts[new_pair] = new_counts.get(new_pair, 0) + count
        char_counts[insert] = char_counts.get(insert, 0) + count

    pair_counts.update(new_counts)


def max_min_diff(char_counts):
    return max(char_counts.values()) - min(char_counts.values())


def main():
    with open(sys.argv[1]) as f:
        template = f.readline().strip()
        f.readline()

        rules = {}
        for line in f.readlines():
            (a, b), insert = line.strip().split(' -> ')
            rules[a + b] = insert

    char_counts = {elem: template.count(elem) for elem in set(template)}
    pair_counts = {pair: 0 for pair in rules.keys()}
    for a, b in zip(template[:-1], template[1:]):
        pair_counts[a + b] += 1

    for _ in range(10):
        grow_polymer(pair_counts, char_counts, rules)
    print('After 10 steps:', max_min_diff(char_counts))

    for _ in range(30):
        grow_polymer(pair_counts, char_counts, rules)
    print('After 40 steps:', max_min_diff(char_counts))


if __name__ == '__main__':
    main()
