from lib import advent
from io import TextIOWrapper
from collections import defaultdict
import math

@advent.parser(15)
def parse(file: TextIOWrapper):
    a = int(file.readline().split()[-1])
    b = int(file.readline().split()[-1])
    return (a, b)


@advent.solver(15, part=1)
def solve1(a: int, b: int):
    factor_a = 16807
    factor_b = 48271
    mod = 2**31-1
    mask = 2**16-1
    count = 0

    # repeats of this are the same as
    for _ in range(40_000_000):
        a = (a * factor_a) % mod
        b = (b * factor_b) % mod

        if (a & mask) == (b & mask):
            count += 1
    return count


@advent.solver(15, part=2, reparse=False)
def solve2(a: int, b: int):
    factor_a = 16807
    factor_b = 48271
    mask = 2**16-1
    count = 0

    agen = generate_mod(a, factor_a, 4)
    bgen = generate_mod(b, factor_b, 8)
    for _ in range(5_000_000):
        a = next(agen)
        b = next(bgen)
        if (a & mask) == (b & mask):
            count += 1
    return count        


def generate_mod(a: int, factor: int, mult: int):
    mod = 2**31-1
    while True:
        a = (a * factor) % mod
        while a % mult != 0:
            a = (a * factor) % mod
        yield a
