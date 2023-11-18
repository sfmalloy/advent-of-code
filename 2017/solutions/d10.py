from .lib.advent import advent
from io import TextIOWrapper


TEST = False

@advent.parser(10)
def parse(file: TextIOWrapper):
    return map(int, file.read().strip().split(','))


@advent.day(10, part=1)
def solve1(lengths: list[int]):
    elems = [i for i in range(256 if not TEST else 5)]
    start = 0
    skip = 0
    for l in lengths:
        end = (start+l-1)
        print(start,elems)
        reverse_sublist(start, end, elems)
        start += l + skip
        skip += 1
    return elems[0] * elems[1]


@advent.day(10, part=2)
def solve2(lengths: list[int]):
    lengths = [ord(str(l)) for l in lengths] + [17,31,73,47,23]
    print(lengths)
    return 0


def reverse_sublist(start: int, end: int, elems: list[int]):
    while end > start:
        elems[start % len(elems)], elems[end % len(elems)] = elems[end % len(elems)], elems[start % len(elems)]
        start += 1
        end -= 1
