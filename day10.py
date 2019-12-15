import collections
import numpy as np
import math
from utils import read_lines, lmap

def compute_k(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    if y1 == y2:
        slope = (x1-x2) * np.inf
    else:
        slope = (x1-x2)/(y1-y2)

    if y1 >= y2:
        return slope, 0
    else:
        return slope, 1


def compute_angle(p):
    angle = math.degrees(math.atan2(p[0], -p[1]))
    if angle < 0:
        angle = 360 + angle
    return angle


def compute_angles_group(group, best):
    group = np.array(group)
    a = group.copy()
    a[:, 0] -= best[0]
    a[:, 1] -= best[1]
    angle = compute_angle(a[0])
    ix = np.argsort([np.abs(i).sum() for i in a])

    ret = []
    for i in group[ix]:
        ret.append((angle, tuple(i)))
        angle += 360
    return ret

def main():
    m = {'#': 1, '.': 0}
    l = lmap(lambda x: [m[i] for i in x[:-1]], read_lines())
    ast = []

    for i in range(len(l)):
        for j in range(len(l[0])):
            if l[i][j]:
                ast.append((j,i))

    s = []
    for i in ast:
        angles = set()
        for j in ast:
            if i != j:
                k = compute_k(i,j)
                angles.add(k)
        s.append(len(angles))

    i = np.argmax(s)
    print(s[i])

    best = ast[i]
    dd = collections.defaultdict(list)
    for i in ast:
        if i != best:
            k = compute_k(i,best)
            dd[k].append(i)

    d = dict(dd)
    s = sorted([j for i in d.values() for j in compute_angles_group(i, best)])
    print(s[199][1])

if __name__ == '__main__':
    main()
