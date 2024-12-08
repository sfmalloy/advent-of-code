from lib import advent
from io import TextIOWrapper


@advent.parser(17)
def parse(file: TextIOWrapper):
    return int(file.read())


@advent.solver(17, part=1)
def solve1(ipt: int) -> int:
    return value_after(ipt, 2017, False)


@advent.solver(17, part=2)
def solve2(ipt: int) -> int:
    return value_after(ipt, 50_000_000, True)


def value_after(ipt: int, limit: int, part2: bool):
    i = 0
    for l in range(1, limit+1):
        i += (ipt + 1)
        i %= l
    goal = 0 if part2 else i
    while True:
        i -= (1 + ipt)
        i %= l
        if i < goal:
            goal -= 1
        l -= 1
        if goal == i:
            return l
