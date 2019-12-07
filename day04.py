
r = 136760,595730

def desc(x):
    p = x[0]
    eq = 0
    l = set()
    for i in x[1:]:
        if p == i:
            eq += 1
        elif p > i:
            return False
        else:
            l.add(eq)
            eq = 0
        p = i
    l.add(eq)
    return 1 in l

cnt = 0
for i in range(*r):
    if desc(str(i)):
        cnt += 1
print(cnt)
