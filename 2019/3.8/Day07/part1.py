def run(p, user_input): 
    add = 1
    mult = 2
    readin = 3
    out = 4
    jump_if_true = 5
    jump_if_false = 6
    less_than = 7
    equals = 8
    halt = 99

    i = 0
    opcode = 0
    output = 0
    while (opcode != halt):
        instr = p[i]
        opcode = p[i] % 100
        instr = instr // 100
        param_modes = [int(x) for x in str(instr)]
        param_modes.reverse()
        
        while (len(param_modes) < 3):
            param_modes.append(0)
        
        if (opcode != halt):
            if (opcode == add or opcode == mult):
                a = p[i + 1] if param_modes[0] == 1 else p[p[i + 1]]
                b = p[i + 2] if param_modes[1] == 1 else p[p[i + 2]]
                pos = p[i + 3] 
                
                p[pos] = a + b if opcode == add else a * b
                i += 4
            elif (opcode == readin):
                p[i + 1 if param_modes[0] == 1 else p[i + 1]] = user_input.pop(0)
                i += 2
            elif (opcode == out):
                output = p[i + 1] if param_modes[0] == 1 else p[p[i + 1]]
                i += 2
            elif (opcode == jump_if_true or opcode == jump_if_false):
                test = p[i + 1] if param_modes[0] == 1 else p[p[i + 1]]
                pos = p[i + 2] if param_modes[1] == 1 else p[p[i + 2]]

                if ((opcode == jump_if_true and test != 0) or (opcode == jump_if_false and test == 0)):
                    i = pos
                else:
                    i += 3
            elif (opcode == less_than or opcode == equals):
                a = p[i + 1] if param_modes[0] == 1 else p[p[i + 1]]
                b = p[i + 2] if param_modes[1] == 1 else p[p[i + 2]]
                pos = p[i + 3]

                if ((opcode == less_than and a < b) or (opcode == equals and a == b)):
                    p[pos] = 1
                else:
                    p[pos] = 0
                
                i += 4
    return output

def next_perm(lst):
    perm = lst.copy()
    k = -1
    for i in range(len(perm) - 1):
        if (perm[i] < perm[i + 1]):
            k = i
    
    if (k == -1):
        return perm
    
    l = -1
    for i in range(k + 1, len(perm)):
        if (perm[k] < perm[i]):
            l = i

    temp = perm[k]
    perm[k] = perm[l]
    perm[l] = temp

    begin_list = perm[:k+1]
    end_list = perm[k+1:]
    end_list.reverse()
    
    return begin_list + end_list

p = list(map(int, open("7.in", 'r').read().strip().split(',')))

perm = [0,1,2,3,4]
max_out = float("-inf")
for i in range(120):
    signal = 0
    for phase in perm:
        signal = run(p.copy(), [phase, signal])
    max_out = max(max_out, signal)
    perm = next_perm(perm)

print("Part 1: %d" % max_out)
