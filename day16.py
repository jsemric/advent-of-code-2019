from functools import lru_cache
import numpy as np
from utils import lmap

def task2(inp):
    pos = sum(10**(6-i)*j for i,j in enumerate(inp[:7]))
    n = inp.shape[0]
    idx = pos % n
    m = 10000 * n
    inp = np.hstack([inp[idx:], np.tile(inp, int((m-pos) // n))])
    assert inp.shape[0] == m - pos

    for j in range(100):
        # pattern will be ones for every entry as the message position is too high
        inp = np.cumsum(inp[::-1])[::-1] % 10
    return int(''.join([str(i) for i in inp[:8]]))

def task1(inp):
    # slow and lazy solution
    n = len(inp)

    for j in range(100):
        out = []
        for i in range(1, n + 1):
            ptrn = generate_pattern(i)
            a = np.tile(ptrn, int(np.ceil(n / len(ptrn))))
            ret = inp[i-1:] * a[:n-i+1]
            out.append(np.abs(np.sum(ret)) % 10)
        inp = np.array(out, dtype=np.int32)

    return int(''.join([str(i) for i in inp[:8]]))

@lru_cache(maxsize=None)
def generate_pattern(i):
    return [1]*i + [0]*i +[-1]*i +[0]*i

def main():
    inp = np.array(lmap(int, input()))
    res = task1(inp)
    print("1.)", res)
    res = task2(inp)
    print("2.)", res)

if __name__ == '__main__':
    main()
