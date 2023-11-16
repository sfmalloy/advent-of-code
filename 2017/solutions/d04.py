from .lib.advent import advent
from io import TextIOWrapper


@advent.parser(4)
def parse(file: TextIOWrapper):
    return [line.strip().split() for line in file.readlines()]

@advent.day(4, part=1)
def solve1(lines: list[str]):
    return sum(len(set(line)) == len(line) for line in lines)

@advent.day(4, part=2)
def solve2(lines: list[str]):
    return sum(len(set(''.join(sorted(word)) for word in line)) == len(line) 
               for line in lines)
