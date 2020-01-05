import numpy as np

from utils import lmap, read_lines

BUG = ord('#')
SPACE = ord('.')
N = 5

def is_bug(a): return a == BUG

def bugs_neigh(grid, x, y):
    return sum([
        is_bug(grid[x - 1, y] if x > 0 else 0),
        is_bug(grid[x+1, y] if x + 1 < N else 0),
        is_bug(grid[x, y - 1] if y > 0 else 0),
        is_bug(grid[x, y + 1] if y + 1 < N else 0),
    ])


def step(grid, **kwargs):
    ret = grid.copy()
    for i in range(N):
        for j in range(N):
            n_bugs = bugs_neigh(grid, i, j, **kwargs)
            if grid[i, j] == BUG:
                if n_bugs != 1:
                    ret[i, j] = SPACE

            elif grid[i, j] == SPACE:
                if n_bugs == 1 or n_bugs == 2:
                    ret[i, j] = BUG

            else:
                raise ValueError()

    return ret

def get_hash(grid):
    return hash(tuple(lmap(tuple, grid)))


def biodiversity(grid):
    return np.sum(np.equal(grid, BUG) * np.reshape(2**np.arange(25), (5,5)))


def task1(grid):
    seen = set()
    for i in range(100):
        grid = step(grid)
        h = get_hash(grid)
        if h in seen:
            break

        seen.add(h)

    return biodiversity(grid)

# part 2 code

def count_bugs(a): return np.sum(a == BUG)

class Grid:

    def __init__(self, grid=None, level=0):
        self.level = level
        self.grid = grid if grid is not None else np.full((N, N), SPACE)
        self.grid[2,2] = ord('?')
        self.uppergrid = None
        self.subgrid = None


    def mid_tiles_bugs(self, move):
        if self.uppergrid is None:
            return 0

        if move == 'up':
            return int(self.uppergrid.grid[1,2] == BUG)
        if move == 'right':
            return int(self.uppergrid.grid[2,3] == BUG)
        if move == 'down':
            return int(self.uppergrid.grid[3,2] == BUG)
        if move == 'left':
            return int(self.uppergrid.grid[2,1] == BUG)
        raise ValueError()


    def edge_tiles_bugs(self, move):
        if self.subgrid is None:
            return 0

        if move == 'down':
            return count_bugs(self.subgrid.grid[0, :])
        if move == 'left':
            return count_bugs(self.subgrid.grid[:, 4])
        if move == 'up':
            return count_bugs(self.subgrid.grid[4, :])
        if move == 'right':
            return count_bugs(self.subgrid.grid[:, 0])
        raise ValueError()


    def bugs(self, x, y, d):
        if x == 2 and y == 2:
            r = self.edge_tiles_bugs(d)
            return r
        elif x < 0 or x == N or y == N or y < 0:
            return self.mid_tiles_bugs(d)

        return int(self.grid[x, y] == BUG)


    def bugs_neigh(self, x, y):
        it = [(x + 1, y, 'down'), (x - 1, y, 'up'), (x, y + 1, 'right'), (x, y - 1, 'left')]
        return sum(self.bugs(i, j, d) for i,j,d in it)


    def update_grid(self):
        grid = self.grid
        ret = grid.copy()
        for i in range(N):
            for j in range(N):
                if i == 2 and j == 2:
                    continue
                n_bugs = self.bugs_neigh(i, j)
                if grid[i, j] == BUG:
                    if n_bugs != 1:
                        ret[i, j] = SPACE

                elif grid[i, j] == SPACE:
                    if n_bugs == 1 or n_bugs == 2:
                        ret[i, j] = BUG

                else:
                    raise ValueError()

        return ret


    def step(self):
        g = self.update_grid()

        if self.level >= 0:
            if self.subgrid is not None:
                self.subgrid.step()
            elif np.equal(self.grid, BUG).any():
                self.subgrid = Grid(level=self.level + 1)
                self.subgrid.uppergrid = self
                self.subgrid.step()

        if self.level <= 0:
            if self.uppergrid is not None:
                self.uppergrid.step()
            elif np.equal(self.grid, BUG).any():
                self.uppergrid = Grid(level=self.level - 1)
                self.uppergrid.subgrid = self
                self.uppergrid.step()

        self.grid = g


    def count_bugs(self):
        s = np.equal(self.grid, BUG).sum()
        if self.level >= 0 and self.subgrid:
            s += self.subgrid.count_bugs()
        if self.level <= 0 and self.uppergrid:
            s += self.uppergrid.count_bugs()
        return s

    def render_grid(self):
        l = []
        for i in range(N):
            s = ''.join(map(lambda x: chr(x), self.grid[i]))
            s += '   '

            for j in range(N):
                if j == i and i == 2:
                    s += '?'
                else:
                    s += str(self.bugs_neigh(i, j))

            l.append(s)
        return '\n'.join(l)

    def print_level(self):
        if self.level <= 0 and self.uppergrid:
            self.uppergrid.print_level()

        print('level', self.level)
        print(self.render_grid())
        print()

        if self.level >= 0 and self.subgrid:
            self.subgrid.print_level()


def task2(grid):
    grid[2,2] = ord('?')
    g = Grid(grid)
    for i in range(200):
        g.step()

    return g.count_bugs()

def main():
    grid = np.array(lmap(
        lambda x: lmap(ord, list(x[:-1])),
        read_lines()
    ))
    print("1.)", task1(grid))
    print("2.)", task2(grid))

main()
