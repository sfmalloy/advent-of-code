from io import TextIOWrapper
from dataclasses import dataclass


@dataclass
class Instruction:
    opcode: int
    x: int
    y: int = 0


CPY = 0
INC = 1
DEC = 2
JNZ = 3


def run(prog: list[Instruction], mem: list[int]):
    ip = 0
    while ip < len(prog):
        i = prog[ip]
        match (i.opcode & 0b1100) >> 2:
            case 0: # cpy
                x_is_reg = i.opcode & 0b0010
                mem[i.y] = mem[i.x] if i.opcode & 0b0010 else i.x
            case 1: # inc
                mem[i.x] += 1
            case 2: # dec
                mem[i.x] -= 1
            case 3: # jnz
                x_is_reg = i.opcode & 0b0010
                y_is_reg = i.opcode & 0b0001
                x = mem[i.x] if x_is_reg else i.x
                y = mem[i.y] if y_is_reg else i.y
                if x:
                    ip += y
                    ip -= 1
        ip += 1
    return mem


def main(file: TextIOWrapper):
    """
    Opcode: 
        2 bits for operation
        1 bit for first operand being immediate or register
        1 bit for second operand being immediate or register
    """

    registers = 'abcd'
    mem = [0, 0, 0, 0]
    prog: list[Instruction] = []
    for line in file.readlines():
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
                prog.append(Instruction(opcode, x, y))
            case ['inc', x]:
                opcode |= INC

                opcode <<= 1
                opcode |= 1
                x = registers.index(x)
                opcode <<= 1
                prog.append(Instruction(opcode, x))
            case ['dec', x]:
                opcode |= DEC

                opcode <<= 1
                opcode |= 1
                x = registers.index(x)
                opcode <<= 1
                prog.append(Instruction(opcode, x))
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
                prog.append(Instruction(opcode, x, y))

    return run(prog, [0, 0, 0, 0])[0], run(prog, [0, 0, 1, 0])[0]
