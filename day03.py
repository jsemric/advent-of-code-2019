import copy
from dataclasses import dataclass

import numpy as np


@dataclass
class Point:
    x: int
    y: int
    d: int

    def mdist(self, p):
        return abs(self.x - p.x) + abs(self.y - p.y)

def intersects(line1, line2):
    a1, b1 = line1
    a2, b2 = line2

    min1x = min(a1.x, b1.x)
    min1y = min(a1.y, b1.y)
    max1x = max(a1.x, b1.x)
    max1y = max(a1.y, b1.y)

    min2x = min(a2.x, b2.x)
    min2y = min(a2.y, b2.y)
    max2x = max(a2.x, b2.x)
    max2y = max(a2.y, b2.y)

    if min1x < max2x and min1y < max2y and max1x > min2x and max1y > min2y:
        if a1.x == b1.x:
            x = a1.x
            y = a2.y
        else:
            x = a2.x
            y = a1.y

        xpoint = Point(x, y, 0)
        score = b1.mdist(xpoint) + b2.mdist(xpoint) + b1.d + b2.d
        xpoint.d = score
        return xpoint

def trace_wire(wire):
    ret = [Point(0, 0, 0)]

    for i in wire:
        d, offset = i[0], int(i[1:])
        p = copy.deepcopy(ret[-1])
        p.d += offset
        if d == 'U':
            p.x += offset
        elif d =='D':
            p.x -= offset
        elif d == 'R':
            p.y += offset
        elif d =='L':
            p.y -= offset
        else:
            print(d)
            assert False

        ret.append(p)
    return ret

def plot_wires(pts1, pts2, xpoints):
    import matplotlib.pyplot as plt

    def get_pts(pts):
        x = [i.x for i in pts]
        y = [i.y for i in pts]
        return x, y

    x, y = get_pts(pts1)
    plt.plot(y, x, 'bo-')
    x, y = get_pts(pts2)
    plt.plot(y, x, 'ro-')
    x, y = get_pts(xpoints)
    plt.scatter(y, x, marker='x', color='green')
    plt.show()

def main():
    wire1 = input().split(',')
    wire2 = input().split(',')

    pts1 = trace_wire(wire1)
    pts2 = trace_wire(wire2)

    xpoints = []
    for line1 in zip(pts1[1:], pts1[:-1]):
        for line2 in zip(pts2[1:], pts2[:-1]):
            xpoint = intersects(line1, line2)
            if xpoint:
                xpoints.append(xpoint)

    #plot_wires(pts1, pts2, xpoints)

    min_ = min(abs(p.x) + abs(p.y) for p in xpoints)
    print("1.)", min_)
    min_ = min(p.d for p in xpoints)
    print("2.)", min_)


if __name__ == '__main__':
    main()
