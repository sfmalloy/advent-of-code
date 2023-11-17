from .lib.advent import advent
from io import TextIOWrapper


@advent.parser(7)
def parse(file: TextIOWrapper):
    return file.readlines()


@advent.day(7, part=1)
def solve1(ipt):
    return 0


@advent.day(7, part=2)
def solve2(ipt):
    return 0
