import sys
from copy import deepcopy
from utils import lmap
from intcode import IntCodeProgram

def render(x):
    print(''.join(map(chr, x)))

def add_input(prog, x):
    for i in x:
        prog.add_input(ord(i))
    prog.add_input(10)

def powerset(s):
     x = len(s)
     for i in range(1 << x):
         yield [s[j] for j in range(x) if (i & (1 << j))]

def interactive(prog, history):
    out = ""
    prev_prog = prog

    while True:
        try:
            s = input()
            if s == 'b':
                prog = prev_prog
                render(prev_out)
                history.pop()
            elif s == 'q':
                print(history)
                print()
                print('Exiting')
                with open('day25.in', 'w') as f:
                    for i in history[:-1]:
                        f.write(i+'\n')
                break
            else:
                if prog.terminated:
                    break
                prev_prog = deepcopy(prog)
                prev_out = out
                add_input(prog, s)
                out = prog.run()
                render(out)
                history.append(s)
        except EOFError:
            print(history)
            print()
            print('Exiting')
            break

def find_subset(prog, history):
    # items collected by hand
    items = [i[5:] for i in history if 'take' in i]

    for i in powerset(items):
        p = deepcopy(prog)
        for j in i:
            add_input(p, 'drop %s' % j)
            p.run()

        add_input(p, 'south')
        out = p.run()
        if p.terminated:
            print("Items:", i)
            render(out)
            return

def main():
    intcode = lmap(int, open('input').read().split(','))
    intcode.extend([0]*1000)

    prog = IntCodeProgram(intcode.copy())
    out = prog.run()
    render(out)
    history = []

    if len(sys.argv) >= 2:
        with open(sys.argv[1], 'r') as f:
            for i in f:
                i = i[:-1]
                history.append(i)
                add_input(prog, i)
                out = prog.run()

    find_subset(prog, history)


main()
