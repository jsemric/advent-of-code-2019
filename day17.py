import itertools
import numpy as np

from functional import seq

from intcode import IntCodeProgram
from utils import lmap

def update_pos(x, y, move):
    if move == LEFT:
        return (x, y - 1)
    if move == RIGHT:
        return (x, y + 1)
    if move == UP:
        return (x - 1, y)
    if move == DOWN:
        return (x + 1, y)
    raise ValueError()

UP, LEFT, DOWN, RIGHT = range(4)

oposties = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT
}

turn_left = {
    (UP, LEFT),
    (LEFT, DOWN),
    (DOWN, RIGHT),
    (RIGHT, UP),
}

def is_crosspoint(a, i, j):
    return (a[i,j] == 35 and a[i+1,j] == 35 and a[i, j+1] == 35
        and a[i-1, j] == 35 and a[i,j-1] == 35)

def print_map(a):
    print(''.join(lmap(chr, a[1:-1,1:-1].ravel())))

def find_moves(a, pos):
    d = UP
    turn = None
    moves = []
    cnt = 0

    while d is not None:
        next_pos = update_pos(*pos, d)
        if a[next_pos] == ord('#'):
            pos = next_pos
            cnt += 1
        else:
            if cnt:
                moves.append((turn, cnt))
            cnt = 0
            new_d = None
            x, y = pos
            for i in [UP, LEFT, DOWN, RIGHT]:
                if i != oposties[d]:
                    next_pos = update_pos(*pos, i)
                    if a[next_pos] == ord('#'):
                        new_d = i
            turn = 'L' if (d, new_d) in turn_left else 'R'
            d = new_d
    return moves


def task2(intcode):
    intcode[0] = 2
    prog = IntCodeProgram(intcode)
    out = prog.run()
    out = ''.join(lmap(chr, out))
    robot_pos = out.find('^')
    out = lmap(ord, out[:out.find('\n\n')+1])
    i = out.index(ord('\n'))
    a = np.array(out).reshape(-1, i+1)
    robot_pos = robot_pos // a.shape[1] + 1, robot_pos % a.shape[1] + 1
    moves = find_moves(np.pad(a, 1, constant_values=ord('.')), robot_pos)

    # solution found by hand using vim
    m = ('C,A,C,B,C,A,B,C,A,B\n'
        'R,6,L,8,R,10\n'
        'L,8,R,4,R,4,R,6\n'
        'R,12,R,4,R,10,R,12\nn\n')

    for i in m:
        prog.add_input(ord(i))
    out = prog.run()
    return out[-1]


def task1(intcode):
    prog = IntCodeProgram(intcode)
    out = prog.run()
    i = out.index(ord('\n'))
    a = np.array(out[:-1]).reshape(-1, i+1)
    a = a[:, :-1]

    return (seq(itertools.product(range(1, a.shape[0] - 1), range(1, a.shape[1] - 1)))
        .filter(lambda x: is_crosspoint(a, x[0], x[1]))
        .map(lambda x: x[0] * x[1])
        .sum()
    )

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
