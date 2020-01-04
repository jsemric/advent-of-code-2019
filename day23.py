from copy import deepcopy

import numpy as np

from utils import lmap
from intcode import IntCodeProgram

def task1(computers):
    while True:
        q = []
        for pc in computers:
            pc.add_input(-1)
            q.extend(pc.run())

        for ip, x, y in np.reshape(q, (-1, 3)):
            if ip == 255:
                return y
            computers[ip].add_input(x)
            computers[ip].add_input(y)


def task2(computers):
    nat = (None, None)
    nat_delivered = set()

    while True:
        q = []
        for pc in computers:
            pc.add_input(-1)
            q.extend(pc.run())

        if not q:
            if nat in nat_delivered:
                return nat[1]

            nat_delivered.add(nat)
            computers[0].add_input(nat[0])
            computers[0].add_input(nat[1])

        for ip, x, y in np.reshape(q, (-1, 3)):
            if ip == 255:
                nat = (x, y)
            else:
                computers[ip].add_input(x)
                computers[ip].add_input(y)

def main():
    intcode = lmap(int, input().split(','))
    intcode.extend([0]*1000)

    computers = []
    for ip in range(50):
        pc = IntCodeProgram(intcode)
        pc.add_input(ip)
        computers.append(pc)

    print("1.)", task1(deepcopy(computers)))
    print("2.)", task2(computers))


if __name__ == "__main__":
    main()
