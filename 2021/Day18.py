import json
from timeit import default_timer

def find_explodable(num, found=False, d=0, idx=0):
    if isinstance(num, int):
        return idx+(not found), found
    elif isinstance(num, list) and d == 4:
        return idx, True
    idx, found = find_explodable(num[0], found, d+1, idx)
    idx, found = find_explodable(num[1], found, d+1, idx)
    return idx, found

def num_list(num, lst=None):
    if lst == None:
        lst = []
    if isinstance(num, int):
        lst.append(num)
        return lst
    lst = num_list(num[0], lst)
    return num_list(num[1], lst)

def outer_explode(num, e_idx, l_idx, r_idx, l_val, r_val, idx=0, d=0):
    if isinstance(num, int):
        if idx == l_idx:
            num += l_val
        elif idx == r_idx:
            num += r_val
        return num, idx+1
    if idx == e_idx and d == 4:
        return 0, idx+2
    lhs, idx = outer_explode(num[0], e_idx, l_idx, r_idx, l_val, r_val, idx, d+1)
    rhs, idx = outer_explode(num[1], e_idx, l_idx, r_idx, l_val, r_val, idx, d+1)
    return [lhs] + [rhs], idx

def explode(num):
    idx, found = find_explodable(num)
    if found:
        regular_nums = num_list(num)
        num = outer_explode(num, idx, idx-1, idx+2, regular_nums[idx], regular_nums[idx+1])[0]
    return num, found

def split_snail(num, found=False):
    if isinstance(num, int):
        if num >= 10 and not found:
            lhs = num//2
            rhs = lhs if num%2==0 else lhs+1
            return [lhs, rhs], True
        return num, found
    lhs, found = split_snail(num[0], found)
    rhs, found = split_snail(num[1], found)
    return [lhs] + [rhs], found

def add(a, b):
    added = [a, b]
    while True:
        added, changed = explode(added)
        if changed:
            continue
        added, changed = split_snail(added)
        if not changed:
            break
    return added

def magnitude(num):
    if isinstance(num, int):
        return num
    return 3*magnitude(num[0]) + 2*magnitude(num[1])

def main():
    start_time = default_timer()

    numbers = []
    with open('inputs/Day18.in') as f:
        for line in f.readlines():
            # no eval here lol
            numbers.append(json.loads(line.strip()))

    snail_sum = numbers[0]
    for snail in numbers[1:]:
        snail_sum = add(snail_sum, snail)

    max_magnitude = 0
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if i != j:
                max_magnitude = max(max_magnitude, magnitude(add(numbers[i], numbers[j])))
    end_time = default_timer()

    print(magnitude(snail_sum))
    print(max_magnitude)
    print(f'Time: {1000*(end_time-start_time):.3f}ms')

if __name__ == '__main__':
    main()
