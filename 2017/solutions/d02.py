from .lib.advent import advent
from io import TextIOWrapper
from math import gcd


@advent.parser(2)
def parse(file: TextIOWrapper) -> list[list[int]]:
    return [list(map(int, line.split('\t'))) for line in file.readlines()]


@advent.day(2, part=1)
def solve1(rows: list[list[int]]):
    return sum([max(r)-min(r) for r in rows])


@advent.day(2, part=2)
def solve2(rows: list[list[int]]):
    return sum([get_even_div(r) for r in rows])
                    

def get_even_div(row: list[int]):
    for i,a in enumerate(row):
        for b in row[i+1:]:
            div = gcd(a, b)
            if a != b and (div == a or div == b):
                return max(a,b)//min(a,b)
