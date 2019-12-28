#!/usr/bin/env python


import itertools
import heapq
from collections import namedtuple

import numpy as np

from utils import lmap, read_lines


Point = namedtuple('Point', 'x y')

Path = namedtuple('Path', 'distance doors')


def get_surrounding(p: Point):
    return [
        Point(p.x + 1, p.y),
        Point(p.x, p.y + 1),
        Point(p.x - 1, p.y),
        Point(p.x, p.y - 1),
    ]


def find_positions(grid):
    keys = {}
    doors = {}
    starts = []

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            a = grid[i,j]
            if a != '.' and a != '#':
                if a.isupper():
                    doors[a.lower()] = Point(i,j)
                elif a.islower():
                    keys[a] = Point(i,j)
                elif a == '@':
                    starts.append(Point(i,j))
                else:
                    raise ValueError(a)
    return keys, doors, starts


def find_path(grid: np.ndarray, p1: Point, p2: Point):
    s = [(0, p1)]
    visited = {p1: 0}
    paths = {}

    while s:
        dist, p = heapq.heappop(s)
        dist += 1
        for i in get_surrounding(p):
            a = grid[i]
            if a != '#' and visited.get(i, 999999) > dist:
                visited[i] = dist
                heapq.heappush(s, (dist, i))
                paths[i] = p
                if i == p2:
                    doors = []
                    p = p2
                    while p != p1:
                        if grid[p].isupper():
                            doors.append(grid[p].lower())
                        p = paths[p]

                    return dist, set(doors)


def path_finder(distances, allkeys):
    def find_reachable_keys(pos, keys):
        l = allkeys - keys
        for i in l:
            if (pos, i) in distances:
                dist, keys_needed = distances[(pos, i)]
                if keys_needed.issubset(keys):
                    yield (dist, i)
    return find_reachable_keys


def find_min_steps(grid):
    keys, doors, starts = find_positions(grid)
    allkeys = set(keys.keys())

    distances = {}
    for (k1, p1), (k2, p2) in itertools.combinations(keys.items(), 2):
        ret = find_path(grid, p1, p2)
        if ret:
            distances[(k1, k2)] = Path(*ret)
            distances[(k2, k1)] = Path(*ret)


    for i,j in enumerate(starts):
        for (k, p) in keys.items():
            ret = find_path(grid, j, p)
            if ret:
                distances[(f'@{i}', k)] = Path(*ret)

    find_reachable_keys = path_finder(distances, allkeys)


    s = [(0, tuple([f'@{i}' for i,_ in enumerate(starts)]), frozenset())]
    seen = set()

    while s:
        dist, positions, keys = heapq.heappop(s)
        if len(keys) == len(allkeys):
            print(dist)
            break

        for i, pos in enumerate(positions):
            if (pos, keys) in seen:
                continue
            seen.add((pos, keys))
            for (d, key) in find_reachable_keys(pos, keys):
                new_pos = (*positions[:i], key, *positions[i+1:])
                heapq.heappush(s, (d + dist, new_pos, keys | {key}))

def solve(fname):
    with open(fname) as f:
        lines = f.read()

    grid = np.array(lmap(lambda x: list(x), lines.split()))
    find_min_steps(grid)

def main():
    solve('input1.txt')
    solve('input2.txt')

main()
