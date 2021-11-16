# Full Intcode Computer
# Advent of Code 2019
# Sean Malloy

# opcodes
ADD = 1
MULT = 2
RET = 99
IN = 3
OUT = 4
JUMP_TRUE = 5
JUMP_FALSE = 6
LESS_THAN = 7
EQUALS = 8
REL_BASE = 9

param_count = {ADD : 3, MULT : 3, RET : 0, IN : 1, OUT : 1, JUMP_TRUE : 2, JUMP_FALSE : 2, LESS_THAN : 3, EQUALS : 3, REL_BASE : 1}

class Intcode:
    def __init__(self, p):
        self.p = {i:p[i] for i in range(len(p))}
        self.ip = self.rel_base = 0

    def get_pos(self, mode, offset):
        if (mode == 0):
            return self.p[self.ip + offset]
        elif (mode == 1):
            return self.ip + offset
        else:
            return self.p[self.ip + offset] + self.rel_base

    def run(self, readin = [], early_return = False, early_count = 1):
        modes = self.p[self.ip] // 100
        opcode = self.p[self.ip] % 100
        output = []

        while (opcode != RET):
            pos = []
            for i in range(param_count[opcode]):
                mode = modes % 10
                pos.append(self.get_pos(mode, i + 1))
                if (pos[-1] not in self.p):
                    self.p[pos[-1]] = 0
                modes = modes // 10

            if (opcode == ADD):
                self.p[pos[2]] = self.p[pos[0]] + self.p[pos[1]]
                self.ip += 4
            elif (opcode == MULT):
                self.p[pos[2]] = self.p[pos[0]] * self.p[pos[1]]
                self.ip += 4
            elif (opcode == IN):
                self.p[pos[0]] = readin.pop(0)
                self.ip += 2
            elif (opcode == OUT):
                output.append(self.p[pos[0]])
                self.ip += 2
                if (early_return and len(output) == early_count):
                    return output
            elif (opcode == JUMP_TRUE):
                if (self.p[pos[0]] != 0):
                    self.ip = self.p[pos[1]]
                else:
                    self.ip += 3
            elif (opcode == JUMP_FALSE):
                if (self.p[pos[0]] == 0):
                    self.ip = self.p[pos[1]]
                else:
                    self.ip += 3
            elif (opcode == LESS_THAN):
                if (self.p[pos[0]] < self.p[pos[1]]):
                    self.p[pos[2]] = 1
                else:
                    self.p[pos[2]] = 0
                self.ip += 4
            elif (opcode == EQUALS):
                if (self.p[pos[0]] == self.p[pos[1]]):
                    self.p[pos[2]] = 1
                else:
                    self.p[pos[2]] = 0
                self.ip += 4
            elif (opcode == REL_BASE):
                self.rel_base += self.p[pos[0]]
                self.ip += 2

            opcode = self.p[self.ip] % 100
            modes = self.p[self.ip] // 100 
        
        return output
