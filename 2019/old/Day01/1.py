f = open("1.in", 'r')

s1 = s2 = 0
for line in f:
    m = int(line)
    
    s1 += int(m / 3) - 2
    while (m > 2):
        k = int(m / 3) - 2
        if (k > 0):
            s2 += k
        m = k

print("Part 1: %d" % s1)
print("Part 2: %d" % s2)

