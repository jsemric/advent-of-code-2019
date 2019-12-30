import numpy as np

from intcode import IntCodeProgram
from utils import lmap, Point

def make_program(intcode):
    def get_output(x, y):
        prog = IntCodeProgram(intcode.copy())
        prog.add_input(x)
        prog.add_input(y)
        return prog.run()[0]
    return get_output

def task1(intcode):
    get_output = make_program(intcode)
    c = 0
    for i in range(50):
        for j in range(50):
            c += get_output(i, j)

    return c

def task2(intcode):
    get_output = make_program(intcode)
    z = np.zeros((1800, 1800))
    left, right = Point(32, 29), Point(35, 29)
    lefts, rights = [], []

    for i in range(1600):
        z[left.y, left.x: right.x+1] = 1
        x, y = left
        y += 1
        while not get_output(x, y):
            x += 1
        left = Point(x, y)

        x, y = right
        y += 1
        while get_output(x, y):
            x += 1
        right = Point(x-1, y)

        lefts.append(left)
        rights.append(right)

    def is_square(x, y):
        return z[y+99, x+99] == 1 and z[y+99, x] and z[y, x+99]

    for l, r in zip(lefts, rights):
        if r.x - l.x > 100:
            for i in range(l.x, r.x):
                if is_square(i, r.y):
                    pt = Point(i, r.y)
                    return pt.x * 10000 + pt.y


def main():
    line = input()
    intcode = lmap(int, line.split(','))
    intcode.extend([0] * 10000)
    r = task1(intcode)
    print("1.)", r)
    r = task2(intcode)
    print("2.)", r)


if __name__ == '__main__':
    main()
