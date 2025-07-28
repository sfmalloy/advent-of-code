from lib import advent
from lib.common.vec import Vec2, RCDir
from io import TextIOWrapper
from collections import defaultdict

class State:
    CLEAN = 0
    WEAKENED = 1
    INFECTED = 2
    FLAGGED = 3


@advent.parser(22)
def parse(file: TextIOWrapper):
    grid = defaultdict(lambda: defaultdict(int))
    for r, row in enumerate(file.readlines()):
        for c, col in enumerate(row.strip()):
            grid[r][c] = State.INFECTED if col == '#' else State.CLEAN
    return grid


@advent.solver(22, part=1)
def solve1(grid: defaultdict[int, defaultdict[int, int]]):
    caused = 0
    pos = Vec2(len(grid) // 2, len(grid[0]) // 2)
    dir = RCDir.N
    for _ in range(10000):
        if grid[pos.r][pos.c] == State.INFECTED:
            dir = RCDir.clockwise(dir)
        else:
            dir = RCDir.counter_clockwise(dir)
        grid[pos.r][pos.c] = State.CLEAN if grid[pos.r][pos.c] == State.INFECTED else State.INFECTED
        if grid[pos.r][pos.c] == State.INFECTED:
            caused += 1
        pos += dir
    return caused


@advent.solver(22, part=2)
def solve2(grid: defaultdict[int, defaultdict[int, int]]):
    caused = 0
    pos = Vec2(len(grid) // 2, len(grid[0]) // 2)
    dir = RCDir.N
    for _ in range(10000000):
        match grid[pos.r][pos.c]:
            case State.CLEAN:
                grid[pos.r][pos.c] = State.WEAKENED
                dir = RCDir.counter_clockwise(dir)
            case State.WEAKENED:
                grid[pos.r][pos.c] = State.INFECTED
                caused += 1
            case State.INFECTED:
                grid[pos.r][pos.c] = State.FLAGGED
                dir = RCDir.clockwise(dir)
            case State.FLAGGED:
                grid[pos.r][pos.c] = State.CLEAN
                dir *= -1
        pos += dir
    return caused
