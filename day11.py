from collections import defaultdict
import sys
import numpy as np
import matplotlib.pyplot as plt
from utils import lmap

def main():
    line = input()
    sys.stdin = open('/dev/tty')
    intcode = lmap(int, line.split(','))
    intcode.extend([0] * 10000)

#    x = Robot(intcode)
#    x.run_intcode()
#    print(len(x.once_painted))

    x = Robot(intcode, start_panel=1)
    x.run_intcode()

    panels = np.array([k for k,v in x.map.items() if v == 1])
    img = np.zeros((100,100))
    for (i,j) in panels:
        img[i,j] = 1
    #import pdb;pdb.set_trace()

    plt.imshow(img)
    plt.show()

UP, LEFT, DOWN, RIGHT = range(4)

class Robot:

    def __init__(self, intcode, start_panel=0):
        self.intcode = intcode.copy()
        self.iptr = 0
        self.relative_base = 0

        self.map = defaultdict(int)
        self.current_pos = 0, 0
        self.map[self.current_pos] = start_panel
        self.once_painted = set()
        if start_panel:
            self.once_painted.add(self.current_pos)
        self.dir = UP

    def get_val(self, x, mode=0):
        if mode == 0:
            return self.intcode[self.intcode[x]]
        if mode == 1:
            return self.intcode[x]
        if mode == 2:
            return self.intcode[self.relative_base + self.intcode[x]]

        raise ValueError(f"invalid mode: {mode}")

    def set_val(self, x, val, mode=0):
        if mode == 0:
            self.intcode[self.intcode[x]] = val
        elif mode == 2:
            self.intcode[self.relative_base + self.intcode[x]] = val
        else:
            raise ValueError(f"invalid mode: {mode}")

    def run_intcode(self):
        out = []
        while True:
            i = self.iptr
            instr = self.intcode[i]
            op = instr % 100
            mode1 = instr // 100 % 10
            mode2 = instr // 1000 % 10
            mode3 = instr // 10000 % 10
            mode4 = instr // 100000 % 10
            assert mode4 == 0
            assert 0 < op < 10 or op == 99, op
            assert 0 <= mode1 < 3
            assert 0 <= mode2 < 3
            assert 0 <= mode3 < 3

            if op == 1:
                # addition
                val = self.get_val(i+1, mode1) + self.get_val(i+2, mode2)
                self.set_val(i + 3, val, mode3)

            elif op == 2:
                val = self.get_val(i+1, mode1) * self.get_val(i+2, mode2)
                self.set_val(i + 3, val, mode3)
            elif op == 3:
                # camera
                assert mode2 == 0
                x, y = self.current_pos
                self.set_val(i + 1, self.map[(x, y)], mode1)
            elif op == 4:
                # painting
                assert mode2 == 0
                r = self.get_val(i + 1, mode1)
                out.append(r)
            elif op == 5:
                if self.get_val(i+1, mode1):
                    self.iptr = self.get_val(i+2, mode2)
                    continue
            elif op == 6:
                if not self.get_val(i+1, mode1):
                    self.iptr = self.get_val(i+2, mode2)
                    continue
            elif op == 7:
                val = 1*(self.get_val(i+1, mode1) < self.get_val(i+2, mode2))
                self.set_val(i + 3, val, mode3)
            elif op == 8:
                val = 1*(self.get_val(i+1, mode1) == self.get_val(i+2, mode2))
                self.set_val(i + 3, val, mode3)
            elif op == 9:
                self.relative_base += self.get_val(i+1, mode1)
            elif op == 99:
                break
            else:
                raise ValueError('invalid op')

            if op in [3, 4, 9]:
                self.iptr += 2
            elif op in [5, 6]:
                self.iptr += 3
            else:
                self.iptr += 4

            if len(out) == 2:
                x, y = self.current_pos
                # color
                assert 0 <= out[0] <= 1
                assert 0 <= out[1] <= 1
                self.map[(x, y)] = out[0]
                if out[0] == 1:
                    self.once_painted.add((x,y))
                # direction
                d = out[1]
                # go left 90 degrees
                if d == 0:
                    self.dir = (self.dir + 1) % 4

                # go right 90 degress
                elif d == 1:
                    self.dir = (self.dir - 1) % 4

                if self.dir == UP:
                    self.current_pos = x - 1, y
                elif self.dir == RIGHT:
                    self.current_pos = x, y + 1
                elif self.dir == DOWN:
                    self.current_pos = x+1, y
                elif self.dir == LEFT:
                    self.current_pos = x, y - 1
                else:
                    raise ValueError()
                out = []

        return out


if __name__ == '__main__':
    main()
