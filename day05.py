import itertools
from utils import lmap

def input_fn():
    return 1

def main():
    line = input()
    intcode = lmap(int, line.split(','))
    rv = run_intcode(intcode, 1)
    print('1.)', rv)
    rv = run_intcode(intcode, 5)
    print('2.)', rv)


def run_intcode(intcode, inp):
    intcode = intcode.copy()
    def get_val(x, mode=0):
        if mode == 1:
            return intcode[x]
        return intcode[intcode[x]]
    output = []

    i = 0
    while True:
        instr = intcode[i]
        op = instr % 100
        mode1 = instr // 100 % 10
        mode2 = instr // 1000 % 10
        assert 0 < op < 9 or op == 99, op
        assert 0 <= mode1 < 2
        assert 0 <= mode2 < 2
        if op == 1:
            intcode[intcode[i+3]] = get_val(i+1, mode1) + get_val(i+2, mode2)
        elif op == 2:
            intcode[intcode[i+3]] = get_val(i+1, mode1) * get_val(i+2, mode2)
        elif op == 3:
            intcode[intcode[i+1]] = inp
        elif op == 4:
            output.append(intcode[intcode[i+1]])
        elif op == 5:
            if get_val(i+1,mode1):
                i = get_val(i+2,mode2)
                continue
        elif op == 6:
            if not get_val(i+1,mode1):
                i = get_val(i+2,mode2)
                continue
        elif op == 7:
            intcode[intcode[i+3]] = 1*(get_val(i+1, mode1) < get_val(i+2, mode2))
        elif op == 8:
            intcode[intcode[i+3]] = 1*(get_val(i+1, mode1) == get_val(i+2, mode2))
        elif op == 99:
            return output
        else:
            raise ValueError('invalid op')

        if op in [3,4]:
            i += 2
        elif op in [5,6]:
            i += 3
        else:
            i += 4


if __name__ == '__main__':
    main()
