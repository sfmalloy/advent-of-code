def init_program(p):
    dynamic_p = {}
    for i in range(len(p)):
        dynamic_p[i] = p[i]

    return dynamic_p

def intcode(p, user_input, i):
    # Opcodes
    add = 1
    mult = 2
    readin = 3
    out = 4
    jump_if_true = 5
    jump_if_false = 6
    less_than = 7
    equals = 8
    change_rel_base = 9 
    halt = 99

    opcode = 0
    output = []
    rel_base = 0
    while (opcode != halt):
        instr = p[i]
        opcode = p[i] % 100
        instr = instr // 100
        param_modes = [int(x) for x in str(instr)]
        param_modes.reverse()
        
        while (len(param_modes) < 3):
            param_modes.append(0)
        
        if (opcode != halt): 
            # Set parameters given parameter modes
            a_pos = b_pos = r_pos = 0
            a = b = r = extend = 0
            if (param_modes[0] == 0):
                a_pos = p[i + 1]
            elif (param_modes[0] == 1):
                a_pos = i + 1
            else:
                a_pos = p[i + 1] + rel_base
            
            if (a_pos not in p):
                p[a_pos] = 0
            a = p[a_pos]
            print(opcode)

            if (opcode in [add, mult, less_than, equals, jump_if_true, jump_if_false]):
                if (param_modes[1] == 0):
                    b_pos = p[i + 2]
                elif (param_modes[1] == 1):
                    b_pos = i + 2
                else:
                    b_pos = p[i + 2] + rel_base
                
                if (b_pos not in p):
                    p[b_pos] = 0
                b = p[b_pos]
            
            if (opcode in [add, mult, less_than, equals]):
                r = p[i + 3]
                if (param_modes[2] == 2):
                    r += rel_base
                if (r not in p):
                    p[r] = 0
            # Do operation based on opcode
            if (opcode == add or opcode == mult): 
                if (opcode == add):
                    p[r] = a + b
                else:
                    p[r] = a * b
                i += 4
            elif (opcode == readin):
                p[a_pos] = user_input.pop(0)
                i += 2
            elif (opcode == out):
                output.append(a)
                i += 2
                if (len(output) == 2):
                    return output, i
            elif (opcode == jump_if_true or opcode == jump_if_false):
                if ((opcode == jump_if_true and a != 0) or (opcode == jump_if_false and a == 0)):
                    i = b
                else:
                    i += 3
            elif (opcode == less_than or opcode == equals):
                if ((opcode == less_than and a < b) or (opcode == equals and a == b)):
                    p[r] = 1
                else:
                    p[r] = 0
                i += 4
            elif (opcode == change_rel_base):
                rel_base += a
                i += 2
    return output, -1


p = init_program(list(map(int, open("11.in", 'r').read().strip().split(','))))

def get_visited(p, init):
    coord = [0,0]
    compass = 0
    h = [0,1,0,-1]
    v = [1,0,-1,0]
    visited = {}
    output, i = intcode(p, [init], 0)

    while (i != -1):
        visited[tuple(coord)] = output[0]
        compass = (compass + (-1 if output[1] == 0 else 1)) % 4
        coord = [coord[0] + h[compass], coord[1] + v[compass]]
        
        next_input = [0]
        if (tuple(coord) in visited):
            next_input = [visited[tuple(coord)]]
        output, i = intcode(p, next_input, i)
    return visited

print(len(get_visited(p.copy(), 0)))

v = get_visited(p.copy(), 1)
min_y = min_x = 1000000000000 
max_y = max_x = -1000000000000
for c in visited:
    min_y = min(c[1], min_y)
    max_y = max(c[1], max_y)

    min_x = min(c[0], min_x)
    max_x = max(c[0], max_x)

print_chr = {0 : ' ', 1 : chr(9608)}
for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
        curr = (x,y)
        color = 0
       
        if (curr in visited):
            color = visited[curr]
        print(print_chr[color], end='')

    print('')
