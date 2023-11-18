from .lib.advent import advent
from io import TextIOWrapper


@advent.day(10, part=1)
def solve1(file: TextIOWrapper):
    lengths = map(int, file.read().strip().split(','))
    elems = [i for i in range(256)]
    start = 0
    skip = 0
    for l in lengths:
        end = (start+l-1)
        reverse_sublist(start, end, elems)
        start += l + skip
        skip += 1
    return elems[0] * elems[1]


@advent.day(10, part=2)
def solve2(file: TextIOWrapper):
    ascii_input = file.read().strip()
    lengths = []
    for c in ascii_input:
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
