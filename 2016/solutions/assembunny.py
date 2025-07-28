from dataclasses import dataclass

@dataclass
class Instruction:
    opcode: int
    x: int
    y: int = 0
    line: str = None


CPY = 0
INC = 1
DEC = 2
JNZ = 3
TGL = 4
MUL = 5
OUT = 6
ADD = 7

class Assembunny:
    ip: int
    mem: list[int]
    prog: list[Instruction]

    def __init__(self, program: list[str], mem: list[int]):
        self.ip = 0
        self.prog = self.parse(program)
        self.mem = mem


    def run(self, debug=False, step=False) -> tuple[list[Instruction], list[int]]:
        while self.ip >= 0 and self.ip < len(self.prog):
            i = self.prog[self.ip]
            match (i.opcode & 0b11100) >> 2:
                case 0: # cpy
                    x_is_reg = i.opcode & 0b0010
                    y_is_reg = i.opcode & 0b0001
                    self.mem[i.y] = self.mem[i.x] if i.opcode & 0b0010 else i.x
                    if debug:
                        print('cpy', self.mem, self.ip+1)
                case 1: # inc
                    self.mem[i.x] += 1
                    if debug:
                        print('inc', self.mem, self.ip+1)
                case 2: # dec
                    self.mem[i.x] -= 1
                    if debug:
                        print('dec', self.mem, self.ip+1)
                case 3: # jnz
                    x_is_reg = i.opcode & 0b0010
                    y_is_reg = i.opcode & 0b0001
                    x = self.mem[i.x] if x_is_reg else i.x
                    y = self.mem[i.y] if y_is_reg else i.y
                    if x:
                        self.ip += y
                        self.ip -= 1
                    if debug:
                        print('jnz', self.mem, self.ip+1, i.line, (i.opcode & 0b11100) >> 2)
                case 4: # tgl
                    x_is_reg = i.opcode & 0b0010
                    x = self.ip + (self.mem[i.x] if x_is_reg else i.x)
                    if x >= len(self.prog):
                        self.ip += 1
                        continue
                    p = self.prog[x]
                    match (p.opcode & 0b11100) >> 2:
                        case 0 | 5: # cpy
                            p.opcode = (JNZ << 2) | (p.opcode & 0b0011)
                        case 1: # inc
                            p.opcode = (DEC << 2) | (p.opcode & 0b0011)
                        case 2 | 4: # dec or tgl
                            p.opcode = (INC << 2) | (p.opcode & 0b0011)
                        case 3: # jnz
                            p.opcode = (CPY << 2) | (p.opcode & 0b0011)
                    if debug:
                        print('tgl', self.mem, self.ip+1)
                case 5: # mul
                    x_is_reg = i.opcode & 0b0010
                    y_is_reg = i.opcode & 0b0001
                    x = self.mem[i.x] if x_is_reg else i.x
                    y = self.mem[i.y] if y_is_reg else i.y
                    self.mem[i.x] = x * y
                    if debug:
                        print('mul', self.mem, self.ip+1)
                case 6: # out
                    x_is_reg = i.opcode & 0b0010
                    if debug:
                        print('out', self.mem, self.ip+1)
                    self.ip += 1
                    return self.mem[i.x] if x_is_reg else i.x
                case 7: # add
                    x_is_reg = i.opcode & 0b0010
                    y_is_reg = i.opcode & 0b0001
                    x = self.mem[i.x] if x_is_reg else i.x
                    y = self.mem[i.y] if y_is_reg else i.y
                    self.mem[i.x] = x + y
                    if debug:
                        print('mul', self.mem, self.ip+1)

            self.ip += 1
            if debug and step:
                input()
        return None


    def parse(self, program: list[str]):
        """
        Opcode: 
            3 bits for operation (can expand in future if needed)
            1 bit for first operand being immediate or register
            1 bit for second operand being immediate or register
        """

        registers = 'abcd'
        prog: list[Instruction] = []
        for line in program:
            parts = line.split()
            opcode = 0
            match parts:
                case ['cpy', x, y]:
                    opcode |= CPY

                    opcode <<= 1
                    x_is_reg = x in registers
                    opcode |= int(x_is_reg)
                    x = registers.index(x) if x_is_reg else int(x)
                    
                    opcode <<= 1
                    opcode |= 1
                    y = registers.index(y)
                    prog.append(Instruction(opcode, x, y, line=line))
                case ['inc', x]:
                    opcode |= INC

                    opcode <<= 1
                    opcode |= 1
                    x = registers.index(x)
                    opcode <<= 1
                    prog.append(Instruction(opcode, x, line=line))
                case ['dec', x]:
                    opcode |= DEC

                    opcode <<= 1
                    opcode |= 1
                    x = registers.index(x)
                    opcode <<= 1
                    prog.append(Instruction(opcode, x, line=line))
                case ['jnz', x, y]:
                    opcode |= JNZ

                    opcode <<= 1
                    x_is_reg = x in registers
                    opcode |= int(x_is_reg)
                    x = registers.index(x) if x_is_reg else int(x)
                    
                    opcode <<= 1
                    y_is_reg = y in registers
                    opcode |= int(y_is_reg)
                    y = registers.index(y) if y_is_reg else int(y)
                    prog.append(Instruction(opcode, x, y, line=line))
                case ['tgl', x]:
                    opcode |= TGL

                    opcode <<= 1
                    x_is_reg = x in registers
                    opcode |= int(x_is_reg)
                    x = registers.index(x) if x_is_reg else int(x)
                    opcode <<= 1
                    prog.append(Instruction(opcode, x, line=line))
                case ['mul', x, y]:
                    opcode |= MUL
                    
                    opcode <<= 1
                    x_is_reg = x in registers
                    opcode |= int(x_is_reg, line=line)
                    x = registers.index(x) if x_is_reg else int(x)
                    
                    opcode <<= 1
                    y_is_reg = y in registers
                    opcode |= int(y_is_reg)
                    y = registers.index(y) if y_is_reg else int(y)
                    prog.append(Instruction(opcode, x, y, line=line))
                case ['out', x]:
                    opcode |= OUT

                    opcode <<= 1
                    x_is_reg = x in registers
                    opcode |= int(x_is_reg)
                    x = registers.index(x) if x_is_reg else int(x)
                    opcode <<= 1
                    prog.append(Instruction(opcode, x, line=line))
                case ['add', x, y]:
                    opcode |= ADD
                    
                    opcode <<= 1
                    x_is_reg = x in registers
                    opcode |= int(x_is_reg)
                    x = registers.index(x) if x_is_reg else int(x)
                    
                    opcode <<= 1
                    y_is_reg = y in registers
                    opcode |= int(y_is_reg)
                    y = registers.index(y) if y_is_reg else int(y)
                    prog.append(Instruction(opcode, x, y, line=line))

        return prog
