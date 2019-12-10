def intcode(p, user_input):
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

    i = 0
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
            
            if (a_pos > len(p) - 1):
                p.extend([0] * (a_pos - (len(p) - 1)))
            a = p[a_pos]

            if (opcode in [add, mult, less_than, equals, jump_if_true, jump_if_false]):
                if (param_modes[1] == 0):
                    b_pos = p[i + 2]
                elif (param_modes[1] == 1):
                    b_pos = i + 2
                else:
                    b_pos = p[i + 2] + rel_base

                if (b_pos > len(p) - 1):
                    p.extend([0] * (b_pos - (len(p) - 1)))
                b = p[b_pos]
            
            if (opcode in [add, mult, less_than, equals]):
                if (i + 3 > len(p) - 1):
                    p.extend([0] * (i + 3 - (len(p) - 1)))
                if (p[i + 3] > len(p) - 1):
                    p.extend([0] * (p[i + 3] - (len(p) - 1))) 
                r = p[i + 3]
                if (param_modes[2] == 2):
                    r += rel_base
                    if (r > len(p) - 1):
                        p.extend([0] * rel_base)
            
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
    return output
