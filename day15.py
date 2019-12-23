from collections import defaultdict, namedtuple

from intcode import IntCodeProgram
from utils import lmap

Pos = namedtuple('Pos', 'x, y')

def update_pos(pos, move):
    assert 0 < move <= 4
    if move == 1:
        return Pos(pos.x - 1, pos.y)
    if move == 2:
        return Pos(pos.x + 1, pos.y)
    if move == 3:
        return Pos(pos.x, pos.y - 1)
    if move == 4:
        return Pos(pos.x, pos.y + 1)
    raise ValueError()

# inverse moves for backtrack
inverse_moves = {
    -1: 2,
    -2: 1,
    -3: 4,
    -4: 3,
}

def main():
    line = input()
    intcode = lmap(int, line.split(','))
    intcode.extend([0] * 1000)
    O, cost = task1(intcode.copy())
    print("1.)", cost)
    cnt = task2(intcode, O)
    print("2.)", cnt)

def task2(intcode, O):
    program = IntCodeProgram(intcode)

    pos = Pos(0,0)
    states = {pos}
    moves = [1,2,3,4]

    while moves:
        move = moves.pop()
        program.add_input(inverse_moves.get(move, move))
        out = program.run()[0]

        if program.terminated:
            print('terminated')
            break

        if out == 0:
            assert move > 0
            continue

        pos = update_pos(pos, inverse_moves.get(move, move))
        if move < 0:
            continue

        if out == 1 or out == 2:
            moves.append(-move)
            if pos not in states:
                states.add(pos)
                moves.extend(range(1,5))

    cnt = 0
    s = {O}
    seen = {O}
    while s:
        cnt += 1
        q = set()
        for i in s:
            q |= set(update_pos(i, j) for j in range(1,5))
        s = (q & states) - seen
        seen |= q
    return cnt - 1

def task1(intcode):
    program = IntCodeProgram(intcode)

    pos = Pos(0,0)
    states = {pos: 0}
    moves = [1,2,3,4]
    cost = 0

    for i in range(10000000):
        cost = states[pos] + 1
        move = moves.pop()

        program.add_input(inverse_moves.get(move, move))
        out = program.run()[0]

        if program.terminated:
            print('terminated')
            break

        if out == 0:
            assert move > 0
            continue

        pos = update_pos(pos, inverse_moves.get(move, move))
        if move < 0:
            continue

        if out == 1:
            moves.append(-move)
            if pos not in states or states[pos] > cost:
                states[pos] = cost
                moves.extend(range(1,5))
        elif 2 == out:
            return (pos, cost)


if __name__ == '__main__':
    main()
