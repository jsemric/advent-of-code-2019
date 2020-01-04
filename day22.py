#!/usr/bin/env python

from utils import read_lines

def cut(l, n):
    return l[n:] + l[:n]

def increment(l, n):
    N = len(l)
    ret = [-1] * N
    i = 0
    idx = 0
    while i < N:
        if ret[idx % N] == -1:
            ret[idx % N] = l[i]
            i += 1
        else: assert False
        idx += n
    return ret

def new_stack(l):
    return list(reversed(l))


def shuffle(l, inp):
    for i in inp:
        if 'cut' in i:
            n = int(i.split()[-1])
            l = cut(l, n)
        elif 'increment' in i:
            n = int(i.split()[-1])
            l = increment(l, n)
        elif 'new' in i:
            l = new_stack(l)
        else:
            raise ValueError(i)
    return l

l = list(range(10007))
lines = list(read_lines())
l = shuffle(l, lines)
print("1.)", l.index(2019))
