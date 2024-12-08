from lib import advent
from io import TextIOWrapper
from collections import deque, defaultdict


@advent.parser(17)
def parse(file: TextIOWrapper):
    return [line.strip() for line in file.readlines()]


@advent.solver(17, part=1)
def solve1(ipt):
    return 0


@advent.solver(17, part=2)
def solve2(ipt):
    return 0
