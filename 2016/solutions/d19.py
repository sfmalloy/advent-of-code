import math
from io import TextIOWrapper


def part1(elves: int):
    return (2*elves + 1) % 2**int(math.log2(elves))


def part2(elves: int):
    pow3 = 3**int(math.log(elves, 3))
    if elves <= pow3 * 2:
        return elves - pow3
    return 2*elves - 3*pow3


def main(file: TextIOWrapper):
    elves = int(file.read())
    return part1(elves), part2(elves)
