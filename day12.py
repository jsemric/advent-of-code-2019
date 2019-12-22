import itertools
import re
import numpy as np
from utils import read_lines, lmap

def parse(x):
    return lmap(int, re.sub('[^\d, -]', '', x).split(', '))

def compute_gravity(pos):
    n = len(pos)
    gravity = np.zeros_like(pos)
    for i, j in itertools.combinations(range(n), 2):
        x = (pos[i] > pos[j])*1 + (pos[i] < pos[j])*(-1)
        gravity[i] += -x
        gravity[j] += x
    return gravity

def main():
    pos = np.array(lmap(parse, read_lines()), dtype=np.int32)
    vel = np.zeros_like(pos, np.int32)
    initial_pos = pos.copy()
    periods = np.zeros(pos.shape[1], np.int64)
    periods_left = list(range(pos.shape[1]))
    assert len(periods_left) == 3

    for i in range(1000):
        gravity = compute_gravity(pos)
        vel += gravity
        pos += vel

    vel = np.abs(vel)
    pos = np.abs(pos)
    energy = np.sum(vel.sum(axis=1) * pos.sum(axis=1))
    print("1.)", energy)

    pos = initial_pos.copy()
    vel = np.zeros_like(pos)

    for i in range(240000):
        gravity = compute_gravity(pos)
        vel += gravity
        pos += vel
        period_found = None
        for j in periods_left:
            if np.all(pos[:, j] == initial_pos[:, j]):
                period_found = j
                periods[j] = i + 1
                break # hopefully no similar periods

        if period_found is not None:
            periods_left.remove(period_found)

        if not periods_left:
            break

    periods += 1 # next step starts the period
    lcm = np.lcm(periods[0], np.lcm(periods[1], periods[2]))
    print("2.)", lcm)


if __name__ == '__main__':
    main()
