from lib import advent
from lib.common.vec import Vec2, RCDir
from io import TextIOWrapper


@advent.parser(19)
def parse(file: TextIOWrapper):
    grid = [line for line in file.readlines()]
    return grid, Vec2(0, grid[0].index('|'))


@advent.solver(19)
def solve1(grid: list[str], pos: Vec2):
    dir = RCDir.D
    letters = []
    letter_steps = []
    steps = 1
    while pos.in_bounds_rc(grid):
        symbol = grid[pos.r][pos.c]
        if symbol.isalpha() and symbol not in letters:
            letters.append(symbol)
            letter_steps.append(steps)
        elif symbol == '+':
            new_dir = RCDir.clockwise(dir)
            next_pos = pos + new_dir
            if not next_pos.in_bounds_rc(grid) or grid[next_pos.r][next_pos.c] == ' ':
                new_dir = RCDir.counter_clockwise(dir)
            dir = new_dir
        pos += dir
        steps += 1
    return ''.join(l for l in letters), letter_steps[-1]
