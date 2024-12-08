from lib import advent
from io import TextIOWrapper


@advent.parser(14)
def parse(file: TextIOWrapper):
    ipt = file.read().strip()
    grid = [list(map(int, bin(int(knot_hash(f'{ipt}-{i}'), base=16))[2:])) for i in range(128)]
    for r in range(len(grid)):
        if len(grid[r]) < 128:
            grid[r] = [0]*(128-len(grid[r])) + grid[r]
    return grid

@advent.solver(14)
def solve(grid: list[list[int]]):
    total = 0
    label = 2
    for i,row in enumerate(grid):
        for j,col in enumerate(row):
            if col == 1:
                walk(i, j, label, grid)
                label += 1
            if col != 0:
                total += 1
    return total, label-2


def walk(i: int, j: int, label: int, grid: list[list[int]]):
    grid[i][j] = label
    if i-1 >= 0 and grid[i-1][j] == 1:
        walk(i-1, j, label, grid)
    if i+1 < len(grid) and grid[i+1][j] == 1:
        walk(i+1, j, label, grid)
    if j-1 >= 0 and grid[i][j-1] == 1:
        walk(i, j-1, label, grid)
    if j+1 < len(grid[0]) and grid[i][j+1] == 1:
        walk(i, j+1, label, grid)


def knot_hash(ipt: str):
    lengths = []
    for c in ipt:
        lengths.append(ord(c))
    lengths += [17, 31, 73, 47, 23]
    elems = [i for i in range(256)]
    start = 0
    skip = 0

    for _ in range(64):
        for l in lengths:
            end = (start+l-1)
            reverse_sublist(start, end, elems)
            start += l + skip
            skip += 1

    ans = ''
    for i in range(0, len(elems), 16):
        ans += dense_hash(i, i+16, elems)

    return ans


def reverse_sublist(start: int, end: int, elems: list[int]):
    while end > start:
        elems[start % len(elems)], elems[end % len(elems)] = elems[end % len(elems)], elems[start % len(elems)]
        start += 1
        end -= 1


def dense_hash(start: int, end: int, elems: list[int]):
    h = 0
    for e in range(start, end):
        h ^= elems[e]
    return f'{hex(h)[2:]:0>2}'

