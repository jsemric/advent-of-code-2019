from collections import defaultdict
import networkx as nx
from utils import lmap, read_lines


def task1(l):
    d = defaultdict(set)
    for i in l:
        d[i[1]].add(i[0])
        d[i[0]]
    d = dict(d)
    cond = True
    while cond:
        cond = False
        for k,v in d.items():
            l = len(d[k])
            for i in v.copy():
                d[k] |= d[i]
            if len(d[k]) != l:
                cond = True

    print('1.)', sum(map(len, d.values())))


def task2(l):
    g = nx.Graph()
    for i in l:
        g.add_edge(i[1],i[0])

    x = nx.shortest_path_length(g, 'SAN', 'YOU')
    print('2.)', x-2)

l = lmap(lambda x: tuple(x.strip().split(')')), read_lines())
task1(l)
task2(l)

