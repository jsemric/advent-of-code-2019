import itertools
from utils import lmap

def main():
    line = input()
    intcode = lmap(int, line.split(','))

    r = run_intcode(intcode)
    print('1.)', r)

    for n,v in itertools.product(range(100), range(100)):
        r = run_intcode(intcode, n, v)
        if r == 19690720:
            print('2.)', n*100 + v)
            break


def run_intcode(intcode, noun=12, verb=2):
    intcode = intcode.copy()
    get_val = lambda x: intcode[intcode[x]]
    intcode[1] = noun
    intcode[2] = verb

    i = 0
    while True:
        op = intcode[i]
        if op == 1:
            intcode[intcode[i+3]] = get_val(i+1) + get_val(i+2)
        elif op == 2:
            intcode[intcode[i+3]] = get_val(i+1) * get_val(i+2)
        elif op == 99:
            return intcode[0]
        else:
            raise ValueError('invalid op')
        i += 4


if __name__ == '__main__':
    main()
