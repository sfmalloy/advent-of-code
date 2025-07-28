from lib import advent
from io import TextIOWrapper
from itertools import batched


@advent.parser(21)
def parse(file: TextIOWrapper):
    return dict(tuple(line.strip().split(' => ')) for line in file.readlines())


@advent.solver(21, part=1)
def solve1(rules: dict[str, str]):
    return process(rules, 5)


@advent.solver(21, part=2)
def solve2(rules: dict[str, str]):
    return process(rules, 18)


def search_rules(rules: dict[str, str], unit: list[tuple[str]]):
    for _ in range(4):
        key = '/'.join(''.join(row) for row in unit)
        if key in rules:
            return rules[key].split('/')
        unit = rotate(unit)
    unit = list(reversed(unit))
    for _ in range(4):
        key = '/'.join(''.join(row) for row in unit)
        if key in rules:
            return rules[key].split('/')
        unit = rotate(unit)


def rotate(unit: list[tuple[str]]):
    return list(reversed(list(zip(*unit))))


def process(rules: dict, iters: int):
    grid = ['.#.','..#','###']
    for _ in range(iters):
        size = 2 if len(grid) % 2 == 0 else 3
        R = len(grid) // size
        C = R
        cols = [[] for _ in range(C)]
        for row in grid:
            for c, col in enumerate(batched(row, size)):
                cols[c].append(col)
        grids = []
        for c in range(len(cols)):
            col = cols[c]
            for b in batched(col, size):
                grids.append(list(b))
        for r in range(len(grids)):
            grids[r] = search_rules(rules, grids[r])
        grid = []
        grids = fix_columns(grids, C)
        for b in batched(grids, R):
            for thing in zip(*b):
                grid.append(''.join(thing))
    
    total = 0
    for row in grid:
        for col in row:
            total += 1 if col == '#' else 0
    return total


def fix_columns(grid, C):
    new_grid = []
    for c in range(C):
        for cc in range(c, c+len(grid), C):
            new_grid.append(grid[cc])
    return new_grid
