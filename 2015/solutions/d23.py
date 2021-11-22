from io import TextIOWrapper

def run(prog, a, b):
    reg = {'a': a, 'b': b}
    ip = 0

    while ip < len(prog):
        ins = prog[ip][0]
        dst = prog[ip][1]
        src = '' if ins not in ['jie','jio'] else prog[ip][2]
        if ins == 'hlf':
            reg[dst] //= 2
            ip += 1
        elif ins == 'tpl':
            reg[dst] *= 3
            ip += 1
        elif ins == 'inc':
            reg[dst] += 1
            ip += 1
        elif ins == 'jmp':
            ip += int(dst)
        elif ins == 'jie':
            ip += int(src) if reg[dst] & 1 == 0 else 1
        elif ins == 'jio':
            ip += int(src) if reg[dst] == 1 else 1

    return reg['b']

def main(in_file: TextIOWrapper):
    prog = [''.join(filter(lambda s: s != ',', l.strip())).split() for l in in_file.readlines()]

    print(run(prog, 0, 0))
    print(run(prog, 1, 0))
