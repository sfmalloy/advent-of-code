from intcode import run

p = list(map(int, open("7.in", 'r').read().strip().split(',')))

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

perm = [0,1,2,3,4]
max_out = float("-inf")
for i in range(120):
    signal = 0
    for phase in perm:
        signal = run(p.copy(), [phase, signal])
    max_out = max(max_out, signal)
    perm = next_perm(perm)

print(max_out)
