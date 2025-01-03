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
TGL = 4
MUL = 5

debug = False

def run(prog: list[Instruction], mem: list[int]) -> tuple[list[Instruction], list[int]]:
    ip = 0
    while ip >= 0 and ip < len(prog):
        i = prog[ip]
        match (i.opcode & 0b11100) >> 2:
            case 0: # cpy
                if debug:
                    print('cpy', mem, ip+1)
                x_is_reg = i.opcode & 0b0010
                y_is_reg = i.opcode & 0b0001
                if not y_is_reg:
                    ip += 1
                    continue
                mem[i.y] = mem[i.x] if i.opcode & 0b0010 else i.x
            case 1: # inc
                if debug:
                    print('inc', mem, ip+1)
                mem[i.x] += 1
            case 2: # dec
                if debug:
                    print('dec', mem, ip+1)
                mem[i.x] -= 1
            case 3: # jnz
                if debug:
                    print('jnz', mem, ip+1)
                x_is_reg = i.opcode & 0b0010
                y_is_reg = i.opcode & 0b0001
                x = mem[i.x] if x_is_reg else i.x
                y = mem[i.y] if y_is_reg else i.y
                if x:
                    ip += y
                    ip -= 1
            case 4: # tgl
                if debug:
                    print('tgl', mem, ip+1)
                x_is_reg = i.opcode & 0b0010
                x = ip + (mem[i.x] if x_is_reg else i.x)
                if x >= len(prog):
                    ip += 1
                    continue
                p = prog[x]
                match (p.opcode & 0b11100) >> 2:
                    case 0 | 5: # cpy
                        p.opcode = (JNZ << 2) | (p.opcode & 0b0011)
                    case 1: # inc
                        p.opcode = (DEC << 2) | (p.opcode & 0b0011)
                    case 2 | 4: # dec or tgl
                        p.opcode = (INC << 2) | (p.opcode & 0b0011)
                    case 3: # jnz
                        p.opcode = (CPY << 2) | (p.opcode & 0b0011)
            case 5: # mul
                if debug:
                    print('mul', mem, ip+1)
                x_is_reg = i.opcode & 0b0010
                y_is_reg = i.opcode & 0b0001
                x = mem[i.x] if x_is_reg else i.x
                y = mem[i.y] if y_is_reg else i.y
                mem[i.x] = x * y
        ip += 1
        if debug:
            input()
    return mem


def parse(program: list[str]):
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
            case ['tgl', x]:
                opcode |= TGL

                opcode <<= 1
                x_is_reg = x in registers
                opcode |= int(x_is_reg)
                x = registers.index(x) if x_is_reg else int(x)
                opcode <<= 1
                prog.append(Instruction(opcode, x))
            case ['mul', x, y]:
                opcode |= MUL
                
                opcode <<= 1
                x_is_reg = x in registers
                opcode |= int(x_is_reg)
                x = registers.index(x) if x_is_reg else int(x)
                
                opcode <<= 1
                y_is_reg = y in registers
                opcode |= int(y_is_reg)
                y = registers.index(y) if y_is_reg else int(y)
                prog.append(Instruction(opcode, x, y))
    return prog
