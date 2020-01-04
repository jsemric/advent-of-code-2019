#!/usr/bin/env python

from utils import lmap, read_lines
from intcode import IntCodeProgram

#intcode = lmap(int, open('../Inputs/day21.txt').read().split(','))
intcode = lmap(int, input().split(','))
intcode.extend([0]*1000)

def add_input(inp, prog):
    for i in map(ord, inp):
        prog.add_input(i)

def add_commands(cmds, prog, last='WALK'):
    for cmd in cmds:
        add_input(cmd + '\n', prog)
    add_input(f'{last}\n', prog)


task1_script = ('NOT A T',
    'NOT B J',
    'OR T J',
    'NOT C J',
    'OR T J',
    'AND D J'
)


prog = IntCodeProgram(intcode.copy())
add_commands(task1_script, prog, last='WALK')
out = prog.run()
print("1.)", out[-1])

task2_script = (
    # if 3rd is hole and 4 and 5 is solid jump
    'NOT C J',
    'AND D J',
    'AND H J',

    # if 2nd is hole and 4 is solid jump
    'NOT B T',
    'AND D T',
    'OR T J',

    # if next is hole jump
    'NOT A T',
    'OR T J',
)


prog = IntCodeProgram(intcode)
add_commands(task2_script, prog, last='RUN')
out = prog.run()
print("2.)", out[-1])
