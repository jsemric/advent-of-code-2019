from collections import Counter
import numpy as np

from intcode import IntCodeProgram
from utils import lmap

def main():
    line = input()
    intcode = lmap(int, line.split(','))
    intcode.extend([0] * 1000)

    program = IntCodeProgram(intcode)
    out = np.array(program.run())
    out.shape = -1, 3
    d = {(x,y): i for (x,y,i) in out}
    print("1.)", Counter(d.values())[2])

    program = IntCodeProgram(intcode)
    program.intcode[0] = 2
    paddlex = 0
    ballx = 0
    score = 0

    while not program.terminated:
        out = np.array(program.run()).reshape(-1, 3)

        for (x,y,i) in out:
            if x == -1 and y == 0:
                score = i
            elif i == 3:
                paddlex = x
            elif i == 4:
                ballx = x

        if paddlex > ballx:
            joystick = -1
        elif  paddlex < ballx:
            joystick = 1
        else:
            joystick = 0
        program.add_input(joystick)

    print("2.)", score)


if __name__ == '__main__':
    main()
