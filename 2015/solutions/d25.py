from io import TextIOWrapper
from collections import defaultdict

def next(r: int, c: int):
    pass

def main(in_file: TextIOWrapper):
    table = defaultdict(int)
    starting = [
        [20151125,  18749137,  17289845,  30943339,  10071777,  33511524],
        [31916031,  21629792,  16929656,   7726640,  15514188,   4041754],
        [16080970,   8057251,   1601130,   7981243,  11661866,  16474243],
        [24592653,  32451966,  21345942,   9380097,  10600672,  31527494],
        [   77061,  17552253,  28094349,   6899651,   9250759,  31663883],
        [33071741,   6796745,  25397450,  24659492,   1534922,  27995004]
    ]
    for i,r in enumerate(starting):
        for j,c in enumerate(r):
            table[(i+1,j+1)] = c

    line = in_file.readline().strip().split('  ')[-1].split()
    row = int(line[-3][:-1])
    col = int(line[-1][:-1])
    prev = (1, 6)
    r = len(starting)
    c = 1
    while not (r == row and c == col):
        curr = (r, c)
        if table[curr] == 0:
            table[curr] = (table[prev] * 252533) % 33554393
        prev = curr
        if r == 1:
            r = c + 1
            c = 1
        else:
            r -= 1
            c += 1
    curr = (r, c)
    table[curr] = (table[prev] * 252533) % 33554393
    print(table[(row,col)])
    print('Weather machine started')
