from typing import overload

class Opcode:
    def __init__(self, code: int, size: int):
        self.code: int = code
        self.size: int = size

class Mode:
    POSITION  = 0
    IMMEDIATE = 1
    RESULT    = 1
    RELATIVE  = 2

class ReturnCode:
    INPUT  = 0
    OUTPUT = 1
    HALT   = 2

class Memory:
    def __init__(self, data):
        self.data = list(data)

    def check_bounds(self, index):
        if isinstance(index, slice):
            if index.start >= len(self):
                self.data.extend([0] * (index.start - len(self) + 1))
            if index.stop > len(self):
                self.data.extend([0] * (index.stop - len(self)))
        elif isinstance(index, int) and index >= len(self):
            self.data.extend([0] * (index - len(self) + 1))
    
    def __getitem__(self, index):
        self.check_bounds(index)
        return self.data[index]
    
    def __setitem__(self, index, value: int):
        self.check_bounds(index)
        self.data[index] = value

    def __len__(self):
        return len(self.data)

    def copy(self):
        new_memory = Memory(self.data.copy())
        return new_memory

class Intcode:
    # Opcodes
    ADD = Opcode(1, 4)
    MUL = Opcode(2, 4)
    IPT = Opcode(3, 2)
    OUT = Opcode(4, 2)
    JIT = Opcode(5, 3)
    JIF = Opcode(6, 3)
    LT  = Opcode(7, 4)
    EQ  = Opcode(8, 4)
    REL = Opcode(9, 2)
    HLT = Opcode(99, 0)

    def __init__(self, program: str):
        self.program = Memory(map(int, program.strip().split(',')))
        self.initial_program = self.program.copy()
        self.ip = 0
        self.ipt_ptr = 0
        self.rel_base = 0

        self.input = []
        self.output = []
    def is_finished(self):
        return self.program[self.ip] == Intcode.HLT.code
    def arg(self, offset: int, mode: int, is_result=False) -> int:
        if is_result:
            if mode == Mode.RELATIVE:
                return self.program[self.ip + offset] + self.rel_base
            return self.program[self.ip + offset]
        elif mode == Mode.POSITION:
            return self.program[self.program[self.ip + offset]]
        elif mode == Mode.RELATIVE:
            return self.program[self.program[self.ip + offset] + self.rel_base]
        else:
            return self.program[self.ip + offset]
    def reset(self):
        self.program = self.initial_program.copy()

        self.ip = 0
        self.ipt_ptr = 0
        self.rel_base = 0

        self.input.clear()
        self.output.clear()
    def read_in(self, *data):
        self.input += list(data)
    def read_out(self) -> list[int]:
        return self.output.copy()
    def mode(self, code: int) -> list[int]:
        digits = []
        digits.append(code % 100)
        code //= 100
        while len(digits) < 4:
            digits.append(code % 10)
            code //= 10
        return list(reversed(digits))
    def run(self):
        idx = 0
        while True:
            mode = self.mode(self.program[self.ip])
            match mode:
                case [_, _, _, Intcode.HLT.code]:
                    return ReturnCode.HALT
                case [p3_mode, p2_mode, p1_mode, opcode]:
                    match opcode:
                        case Intcode.ADD.code:
                            res_pos = self.arg(3, p3_mode, is_result=True)
                            self.program[res_pos] = self.arg(1, p1_mode) + self.arg(2, p2_mode)
                            self.ip += Intcode.ADD.size
                        case Intcode.MUL.code:
                            res_pos = self.arg(3, p3_mode, is_result=True)
                            self.program[res_pos] = self.arg(1, p1_mode) * self.arg(2, p2_mode)
                            self.ip += Intcode.MUL.size
                        case Intcode.IPT.code:
                            if self.ipt_ptr == len(self.input):
                                return ReturnCode.INPUT
                            res_pos = self.arg(1, p1_mode, is_result=True)
                            self.program[res_pos] = self.input[self.ipt_ptr]
                            self.ipt_ptr += 1
                            self.ip += Intcode.IPT.size
                        case Intcode.OUT.code:
                            self.output.append(self.arg(1, p1_mode))
                            self.ip += Intcode.OUT.size
                        case Intcode.JIT.code:
                            if self.arg(1, p1_mode) != 0:
                                self.ip = self.arg(2, p2_mode)
                            else:
                                self.ip += Intcode.JIT.size
                        case Intcode.JIF.code:
                            if self.arg(1, p1_mode) == 0:
                                self.ip = self.arg(2, p2_mode)
                            else:
                                self.ip += Intcode.JIF.size
                        case Intcode.LT.code:
                            res_pos = self.arg(3, p3_mode, is_result=True)
                            self.program[res_pos] = int(self.arg(1, p1_mode) < self.arg(2, p2_mode))
                            self.ip += Intcode.LT.size
                        case Intcode.EQ.code:
                            res_pos = self.arg(3, p3_mode, is_result=True)
                            self.program[res_pos] = int(self.arg(1, p1_mode) == self.arg(2, p2_mode))
                            self.ip += Intcode.EQ.size
                        case Intcode.REL.code:
                            self.rel_base += self.arg(1, p1_mode)
                            self.ip += Intcode.REL.size
