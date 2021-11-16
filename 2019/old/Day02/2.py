p = list(map(int, open("2.in", 'r').read().split(',')))                
q = p.copy()

i = 0
op = p[i]
p[1] = 12
p[2] = 2
while (op != 99):
    res = 0

    if (p[i] == 1):
        p[p[i + 3]] = p[p[i + 1]] + p[p[i + 2]]
    elif (p[i] == 2):
        p[p[i + 3]] = p[p[i + 1]] * p[p[i + 2]]
 
    op = p[i]
    i += 4

print("Part 1: %d" % p[0])

p = q.copy()
found = False
for j in range(0, 100):
    for k in range(0, 100):
        i = 0
        p[1] = j
        p[2] = k
        op = p[0]
        while (op != 99):
            res = 0

            if (p[i] == 1):
                p[p[i + 3]] = p[p[i + 1]] + p[p[i + 2]]
            elif (p[i] == 2):
                p[p[i + 3]] = p[p[i + 1]] * p[p[i + 2]]
         
            op = p[i]
            i += 4
        
        if (p[0] == 19690720):
            print ("Part 2: %d" % (100 * j + k))
            found = True
            break
        p = q.copy()

    if (found):
        break
