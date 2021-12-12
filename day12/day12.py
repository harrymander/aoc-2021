#!/usr/bin/env python3

import sys


def num_routes(node, graph, visited=set(), revisit_small=False):
    if node == 'end':
        return 1
    elif node.islower():
        visited = visited | {node}

    count = 0
    for next_node in graph[node]:
        if next_node not in visited:
            count += num_routes(next_node, graph, visited, revisit_small)
        elif revisit_small:
            count += num_routes(next_node, graph, visited, False)

    return count


if __name__ == '__main__':
    graph = {}
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            caves = line.strip().split('-')
            for i in (0, 1):
                cave = caves[i]
                if cave != 'end':
                    other = caves[not i]
                    if other != 'start':
                        graph.setdefault(cave, []).append(other)

    print(num_routes('start', graph, revisit_small=False))
    print(num_routes('start', graph, revisit_small=True))
