from utils import read_lines

def compute_fuel(x):
    a = x // 3 - 2
    if a <= 0:
        return 0
    else:
        return a + compute_fuel(a)

def main():
    lines = list(read_lines()=True)

    print('1.)', sum(int(i) // 3 - 2 for i in lines))
    print('2.)', sum(compute_fuel(int(i)) for i in lines))

if __name__ == '__main__':
    main()
