class Opcode:
    def __init__(self, code, size):
        self.code = code
        self.size = size

class Intcode:
    ADD = Opcode(1, 4)
    MUL = Opcode(2, 4)
    HLT = Opcode(99, 0)
    def __init__(self, program: str):
        self.program = list(map(int, program.split(',')))
        self.initial_program = self.program.copy()
        self.ip = 0
    def arg(self, offset):
        return self.program[self.ip + offset]
    def reset(self):
        self.program = self.initial_program.copy()
        self.ip = 0
    def run(self):
        while self.arg(0) != 99:
            match self.program[self.ip]:
                case Intcode.ADD.code:
                    res_pos = self.arg(3)
                    self.program[res_pos] = self.program[self.arg(1)] + self.program[self.arg(2)]
                    self.ip += Intcode.ADD.size
                case Intcode.MUL.code:
                    res_pos = self.arg(3)
                    self.program[res_pos] = self.program[self.arg(1)] * self.program[self.arg(2)]
                    self.ip += Intcode.MUL.size
