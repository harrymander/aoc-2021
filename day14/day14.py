#!/usr/bin/env python3

import sys


def grow_polymer(template, rules):
    new_template = []
    for i, (a, b) in enumerate(zip(template[:-1], template[1:])):
        insert = rules.get(a + b, None)
        if insert:
            new_template.extend(a + insert)
        else:
            new_template.append(a)
    new_template.append(template[-1])

    return new_template


def max_min_diff(template):
    counts = tuple(template.count(elem) for elem in set(template))
    return max(counts) - min(counts)


def main():
    with open(sys.argv[1]) as f:
        template = f.readline().strip()
        f.readline()

        rules = dict(line.strip().split(' -> ') for line in f.readlines())

    for _ in range(10):
        template = grow_polymer(template, rules)
    print('After 10 steps:', max_min_diff(template))


if __name__ == '__main__':
    main()
