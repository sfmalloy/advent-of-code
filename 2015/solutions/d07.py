from io import TextIOWrapper

def simulate(cmds, init={}):
    wires = init.copy()
    # Cycle through the all of the commands doing them 
    # as inputs become available
    while len(cmds) > 0:
        cmd = cmds.pop(0)
        if cmd[1] in {'AND', 'OR', 'LSHIFT', 'RSHIFT'}:
            a = cmd[0]
            b = cmd[2]
            if a.isnumeric():
                a = int(a)
            elif a in wires:
                a = wires[a]
            else:
                cmds.append(cmd)
                continue
            if b.isnumeric():
                b = int(b)
            elif b in wires:
                b = wires[b]
            else:
                cmds.append(cmd)
                continue
            op = cmd[1]
            c = cmd[4]
            if op == 'AND':
                wires[c] = a & b
            elif op == 'OR':
                wires[c] = a | b
            elif op == 'LSHIFT':
                wires[c] = a << b
            elif op == 'RSHIFT':
                wires[c] = a >> b
        elif cmd[0] == 'NOT':
            a = cmd[1]
            if a.isnumeric():
                a = int(a)
            elif a in wires:
                a = wires[a]
            else:
                cmds.append(cmd)
                continue
            b = cmd[3]
            wires[b] = ~a
        elif cmd[2] not in init:
            a = cmd[0]
            if a.isnumeric():
                a = int(a)
            elif a in wires:
                a = wires[a]
            else:
                cmds.append(cmd)
                continue
            b = cmd[2]
            wires[b] = a
    return wires['a']

def main(in_file: TextIOWrapper):
    cmds = [c.rstrip().split() for c in in_file.readlines()]
    part1 = simulate(cmds.copy())
    print(part1 % 65536)
    print(simulate(cmds.copy(), {'b':part1}))