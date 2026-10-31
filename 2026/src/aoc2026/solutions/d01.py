from io import TextIOWrapper

from ..lib import advent


@advent.parser(1)
def parse(file: TextIOWrapper):
    return [line.strip() for line in file]


@advent.solver(1, part=1)
def solve1(ipt) -> int:
    return 1


@advent.solver(1, part=2)
def solve2(ipt) -> int:
    return 0
