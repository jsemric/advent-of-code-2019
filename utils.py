import sys

def lmap(f, it):
    return list(map(f, it))

def read_lines():
    for i in sys.stdin:
        yield i
