from .lib.advent import advent
from io import TextIOWrapper


@advent.parser(5)
def parse(file: TextIOWrapper):
    return list(map(int, file.readlines()))

@advent.day(5, part=1)
def solve1(jumps: list[int]):
    ip = 0
    steps = 0
    while ip < len(jumps):
        prev = ip
        ip += jumps[ip]
        jumps[prev] += 1
        steps += 1
    return steps


@advent.day(5, part=2)
def solve2(jumps: list[int]):
    ip = 0
    steps = 0
    while ip < len(jumps):
        prev = ip
        ip += jumps[ip]
        if jumps[prev] >= 3:
            jumps[prev] -= 1
        else:
            jumps[prev] += 1
        steps += 1
    return steps
