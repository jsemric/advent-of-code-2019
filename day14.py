from collections import defaultdict, namedtuple
import itertools
import math
import numpy as np
from utils import read_lines, lmap

Material = namedtuple('Material', 'name, amount')

def parse_pair(string):
    n, ch = string.strip().split()
    return Material(name=ch, amount=int(n))

def parse(line):
    inp, out = line.split('=>')
    out = parse_pair(out)
    inp = lmap(parse_pair, inp.split(','))
    return (out.name, (out.amount, inp))


def make_fuel(rules, fuel_amount):
    left = defaultdict(int)
    s = [Material('FUEL', fuel_amount)]
    ores = 0

    while s:
        material = s.pop()
        if material.name == 'ORE':
            ores += material.amount
        elif left[material.name] >= material.amount:
            left[material.name] -= material.amount
        else:
            needed = material.amount - left[material.name]
            n_produced, ingredients = rules[material.name]
            batches = math.ceil(needed / n_produced)
            for i in ingredients:
                s.append(Material(i.name, i.amount * batches))
            left[material.name] = batches * n_produced - needed
    return ores


def main():
    rules = dict(map(parse, read_lines()))
    print("1.)", make_fuel(rules, 1))

    low, upper = 10000, 10000000000
    n = 1000000000000
    while low + 1 != upper:
        mid = (low + upper + 1) // 2
        ores = make_fuel(rules, mid)
        if ores < n:
            low = mid + 1
        else:
            upper = mid

    print("2.)", mid - 1)

if __name__ == '__main__':
    main()
