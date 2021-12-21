import json

def find_explodable(num, d=0, path=[]):
    if isinstance(num, int):
        return None
    elif isinstance(num, list) and d == 4:
        return path
    lhs = find_explodable(num[0], d+1, path + [0])
    rhs = find_explodable(num[1], d+1, path + [1])
    if lhs is not None:
        return lhs
    elif rhs is not None:
        return rhs
    return None

def num_list(num, lst=[]):
    if isinstance(num, int):
        lst.append(num)
        return lst
    lst = num_list(num[0], lst)
    return num_list(num[1], lst)

def explode(num):
    e = find_explodable(num)
    regular_nums = num_list(num)
    idx = sum(e)
    lhs = 0 if idx == 0 else regular_nums[idx-1]
    rhs = 0 if idx+1 == len(regular_nums) else regular_nums[idx+2]


def split(num):
    pass

def add(a, b):
    added = [a, b]
    while True:
        new = explode(add)
        new = split(new)
        if new == added:
            break
        added = new
    return added

numbers = []
with open('inputs/test.in') as f:
    for line in f.readlines():
        numbers.append(json.loads(line.strip()))

explode(numbers[0])

# snail_sum = numbers[0]
# for snail in numbers[1:]:
#     snail_sum = add(snail_sum, snail)
# print(snail_sum)
