# use open("3.in", 'r').read() for file i/o

def get_path(dirs):
    p = []
    curr = [0,0]
    for m in dirs:
        d = m[0]
        dist = int(m[1:])
        
        if (d == 'U'):
            for i in range(1, dist + 1):
                p.append([curr[0], curr[1] + i])
            curr = [curr[0], curr[1] + dist]
        elif (d == 'D'):
            for i in range(1, dist + 1):
                p.append([curr[0], curr[1] - i])
            curr = [curr[0], curr[1] - dist]
        elif (d == 'R'):
            for i in range(1, dist + 1):
                p.append([curr[0] + i, curr[1]])
            curr = [curr[0] + dist, curr[1]]
        else:
            for i in range(1, dist + 1):
                p.append([curr[0] - i, curr[1]])
            curr = [curr[0] - dist, curr[1]]
        
    return p

f = open("3.in", 'r')
a = get_path(f.readline().split(','))
b = get_path(f.readline().split(','))

search_a = set(map(tuple, a))
search_b = set(map(tuple, b))
min_d = float("inf")
ints = []
for c in search_a:
    if (c in search_b):
        if (abs(c[0]) + abs(c[1]) < min_d):
            min_d = abs(c[0]) + abs(c[1])
        ints.append(list(c))

print(min_d)

mindex = float("inf")
print(ints)
for c in ints:
    steps = 2 + a.index(c) + b.index(c)
    if (steps < mindex):
        mindex = steps

print(mindex)
