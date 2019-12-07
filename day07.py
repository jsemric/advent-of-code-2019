import itertools
from utils import lmap


def main():
    line = input()
    intcode = lmap(int, line.split(','))
    task1(intcode)
    task2(intcode)


def task1(intcode):
    max_val = 0
    max_code = [0]*5

    for l in itertools.permutations(range(0,5)):
        r = 0
        for i in l:
            r = IntCodeProgram(intcode, i).run_intcode(r)
        if r > max_val:
            max_val = r
            max_code = l

    print('1.)', max_val, ''.join(map(str,max_code)))


def task2(intcode):
    max_val = 0
    max_code = [0]*5

    for l in itertools.permutations(range(5,10)):
        amplifiers = [IntCodeProgram(intcode, i) for i in l]

        cond = True
        r = 0
        while cond:
            for a in amplifiers:
                ret = a.run_intcode(r)
                if ret is None:
                    cond = False
                    break
                r = ret
        if r > max_val:
            max_val = r
            max_code = l

    print('2.)', max_val, ''.join(map(str,max_code)))


class IntCodeProgram:

    def __init__(self, intcode, first_input):
        self.intcode = intcode.copy()
        self.first_input = first_input
        self.iptr = 0
        self.first_input_sent = False

    def get_val(self, x, mode=0):
        if mode == 1:
            return self.intcode[x]
        return self.intcode[self.intcode[x]]

    def run_intcode(self, inp):
        while True:
            i = self.iptr
            instr = self.intcode[i]
            op = instr % 100
            mode1 = instr // 100 % 10
            mode2 = instr // 1000 % 10
            assert 0 < op < 9 or op == 99, op
            assert 0 <= mode1 < 2
            assert 0 <= mode2 < 2
            if op == 1:
                self.intcode[self.intcode[i+3]] = self.get_val(i+1, mode1) + self.get_val(i+2, mode2)
            elif op == 2:
                self.intcode[self.intcode[i+3]] = self.get_val(i+1, mode1) * self.get_val(i+2, mode2)
            elif op == 3:
                if self.first_input_sent:
                    self.intcode[self.intcode[i+1]] = inp
                else:
                    self.intcode[self.intcode[i+1]] = self.first_input
                    self.first_input_sent = True
            elif op == 4:
                self.iptr += 2
                assert self.first_input_sent
                return self.intcode[self.intcode[i+1]]
            elif op == 5:
                if self.get_val(i+1,mode1):
                    self.iptr = self.get_val(i+2,mode2)
                    continue
            elif op == 6:
                if not self.get_val(i+1,mode1):
                    self.iptr = self.get_val(i+2,mode2)
                    continue
            elif op == 7:
                self.intcode[self.intcode[i+3]] = 1*(self.get_val(i+1, mode1) < self.get_val(i+2, mode2))
            elif op == 8:
                self.intcode[self.intcode[i+3]] = 1*(self.get_val(i+1, mode1) == self.get_val(i+2, mode2))
            elif op == 99:
                return
            else:
                raise ValueError('invalid op')

            if op in [3,4]:
                self.iptr += 2
            elif op in [5,6]:
                self.iptr += 3
            else:
                self.iptr += 4


if __name__ == '__main__':
    main()
