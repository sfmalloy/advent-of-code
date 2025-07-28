from io import TextIOWrapper
from collections import defaultdict


def main(file: TextIOWrapper):
    lines = [line for line in file.readlines()]
    counts = [defaultdict(int) for _ in range(len(lines[0]))]
    for line in lines:
        for i,c in enumerate(line):
            counts[i][c] += 1
    
    p1 = ''
    p2 = ''
    for dct in counts:
        mx = max(dct, key=lambda k:dct[k])
        mn = min(dct, key=lambda k:dct[k])
        p1 += mx
        p2 += mn

    return p1,p2
