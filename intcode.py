from queue import deque

class IntCodeProgram:

    def __init__(self, intcode):
        self.intcode = intcode.copy()
        self.iptr = 0
        self.relative_base = 0

        self.input = deque()
        self.terminated = False

    def get_val(self, x, mode=0):
        if mode == 0:
            return self.intcode[self.intcode[x]]
        if mode == 1:
            return self.intcode[x]
        if mode == 2:
            return self.intcode[self.relative_base + self.intcode[x]]

        raise ValueError(f"invalid mode: {mode}")

    def set_val(self, x, val, mode=0):
        if mode == 0:
            self.intcode[self.intcode[x]] = val
        elif mode == 2:
            self.intcode[self.relative_base + self.intcode[x]] = val
        else:
            raise ValueError(f"invalid mode: {mode}")

    def add_input(self, val):
        self.input.append(val)

    def run(self):
        out = []
        while True:
            i = self.iptr
            instr = self.intcode[i]
            op = instr % 100
            mode1 = instr // 100 % 10
            mode2 = instr // 1000 % 10
            mode3 = instr // 10000 % 10
            mode4 = instr // 100000 % 10
            assert mode4 == 0
            assert 0 < op < 10 or op == 99, op
            assert 0 <= mode1 < 3
            assert 0 <= mode2 < 3
            assert 0 <= mode3 < 3

            if op == 1:
                val = self.get_val(i+1, mode1) + self.get_val(i+2, mode2)
                self.set_val(i + 3, val, mode3)

            elif op == 2:
                val = self.get_val(i+1, mode1) * self.get_val(i+2, mode2)
                self.set_val(i + 3, val, mode3)
            elif op == 3:
                assert mode2 == 0
                if not self.input:
                    return out
                inp = self.input.popleft()
                self.set_val(i + 1, inp, mode1)
            elif op == 4:
                assert mode2 == 0
                r = self.get_val(i + 1, mode1)
                out.append(r)
            elif op == 5:
                if self.get_val(i+1,mode1):
                    self.iptr = self.get_val(i+2,mode2)
                    continue
            elif op == 6:
                if not self.get_val(i+1,mode1):
                    self.iptr = self.get_val(i+2,mode2)
                    continue
            elif op == 7:
                val = 1*(self.get_val(i+1, mode1) < self.get_val(i+2, mode2))
                self.set_val(i + 3, val, mode3)
            elif op == 8:
                val = 1*(self.get_val(i+1, mode1) == self.get_val(i+2, mode2))
                self.set_val(i + 3, val, mode3)
            elif op == 9:
                self.relative_base += self.get_val(i+1, mode1)
            elif op == 99:
                self.terminated = True
                break
            else:
                raise ValueError('invalid op')

            if op in [3,4,9]:
                self.iptr += 2
            elif op in [5,6]:
                self.iptr += 3
            else:
                self.iptr += 4

        return out
