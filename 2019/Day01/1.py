import sys

s1 = s2 = 0
for line in sys.stdin:
    m = int(line)
    
    s1 += int(m / 3) - 2
    while (m > 2):
        k = int(m / 3) - 2
        if (k > 0):
            s2 += k
        m = k

print(s1)
print(s2)
