from .lib.advent import advent
from io import TextIOWrapper


@advent.parser(15)
def parse(file: TextIOWrapper):
    a = int(file.readline().split()[-1])
    b = int(file.readline().split()[-1])
    return (a, b)


@advent.day(15, part=1)
def solve1(generators: tuple[int, int]):
    a, b = generators
    factor_a = 16807
    factor_b = 48271
    mod = 2**31-1
    mask = 2**16-1
    count = 0
    for _ in range(40_000_000):
        a = (a * factor_a) % mod
        b = (b * factor_b) % mod
        if (a & mask == b & mask):
            count += 1
    return count


@advent.day(15, part=2, reparse=False)
def solve2(ipt):
    return 0
