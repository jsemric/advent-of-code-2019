import heapq
from collections import defaultdict

import numpy as np
from utils import lmap, Point, read_lines


def get_neigh(i, j):
    return [
        Point(i,j+1),
        Point(i+1,j),
        Point(i,j-1),
        Point(i-1,j),
    ]


def get_portals(maze):

    def get_closest_path(i, j):
        for i in get_neigh(i, j):
            if maze[i] == ord('.'):
                return i

    dd = defaultdict(set)

    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            a = chr(maze[i,j])
            if a.isupper():

                for pos in get_neigh(i,j):
                    ch = chr(maze[pos])
                    if ch.isupper():
                        portal_name = ''.join(sorted(a + ch))
                        break

                if get_closest_path(*pos) is None:
                    pos = Point(i,j)
                dd[portal_name].add(pos)

    portals = {}
    start_pos = get_closest_path(*list(dd['AA'])[0])

    for k,v in dd.items():
        v = list(v)
        if k == 'AA' or k == 'ZZ':
            portals[v[0]] = k
        else:
            assert len(v) == 2
            a, b = v
            portals[a] = get_closest_path(*b)
            portals[b] = get_closest_path(*a)

    return portals, start_pos, dd


def task1(maze, portals, start_pos):
    s = [(0, start_pos)]
    visited = set()

    while s:
        steps, pos = heapq.heappop(s)
        visited.add(pos)

        for i in get_neigh(*pos):
            ch = chr(maze[i])
            if ch == '.':
                if i not in visited:
                    heapq.heappush(s, (steps+1, i))
            elif ch.isupper():
                n = portals[i]
                if n == 'ZZ':
                    s = []
                    break
                elif n != 'AA':
                    if n not in visited:
                        heapq.heappush(s, (steps+1, n))

    return steps

def task2(maze, portals, start_pos, inner):
    s = [(0, 0, start_pos)]
    visited = set()

    while s:
        steps, level, pos = heapq.heappop(s)
        visited.add((level, pos))


        for i in get_neigh(*pos):

            if (level, i) in visited:
                continue

            ch = chr(maze[i])

            if ch == '.':
                heapq.heappush(s, (steps+1, level, i))
            elif ch.isupper():
                n = portals[i]

                if level == 0 and n == 'ZZ':
                    s = []
                    break
                elif n == 'AA' or n == 'ZZ':
                    continue

                if i in inner:
                    new_level = level + 1
                else:
                    if level == 0:
                        continue
                    new_level = level - 1


                if (new_level, n) not in visited:
                    heapq.heappush(s, (steps+1, new_level, n))

    return steps


def main():
    lines = list(read_lines())
    n = max(map(len, lines))

    maze = np.array([lmap(ord, list(i[:-1])) + [ord(' ')] * (n-len(i)) for i in lines])
    maze = np.pad(maze, 1)

    portals, start_pos, dd = get_portals(maze)
    r = task1(maze, portals, start_pos)
    print("1.)", r)

    def is_outer(pos):
        return (pos.x < 8 or pos.y < 8 or
            pos.x > maze.shape[0]-5 or pos.y > maze.shape[1] - 5)

    outer = {i for i in portals if is_outer(i)}
    inner = {i for i in portals if not is_outer(i)}
    m = {i: k for k,v in dd.items() for i in v}
    assert sorted([m[i] for i in outer])[1:-1] == sorted([m[i] for i in inner])

    r = task2(maze, portals, start_pos, inner)
    print("2.)", r)

main()
