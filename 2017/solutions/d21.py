from lib import advent
from io import TextIOWrapper
from collections import deque, defaultdict
from itertools import batched


@advent.parser(21)
def parse(file: TextIOWrapper):
    return dict(tuple(line.strip().split(' => ')) for line in file.readlines())


@advent.solver(21, part=1)
def solve1(rules: dict[str, str]):
    # grid = ['.#.','..#','###']
    grid = ['#..#', '....', '....', '#..#']
    for _ in range(1):
        size = 2 if len(grid) % 2 == 0 else 3
        lazy = defaultdict(lambda: defaultdict(list))
        for row_subgrid in batched(grid, len(grid)//size):
            for r, row in enumerate(row_subgrid):
                for c, col_subgrid in enumerate(batched(row, size)):
                    lazy[r][c].append(col_subgrid)
        new_grid = defaultdict(lambda: defaultdict(list))
        for r in range(len(lazy)):
            for c in range(len(lazy[r])):
                converted = search_rules(rules, lazy[r][c])
                for elem in converted.split('/'):
                    new_grid[r][c].append(''.join(elem))
        grid = []
        for r in range(len(new_grid)):
            for c in range(len(new_grid[r])):
                grid.append(new_grid[r][c])
        bruh = []
        for r in batched(grid, size):
            bruh.append(list(zip(*r)))
        
        print(bruh)
    return 0


@advent.solver(21, part=2)
def solve2(ipt):
    return 0


def search_rules(rules: dict[str, str], unit: list[tuple[str]]):
    for _ in range(4):
        key = '/'.join(''.join(row) for row in unit)
        if key in rules:
            return rules[key]
        unit = rotate(unit)

    unit = list(reversed(unit))
    for _ in range(4):
        key = '/'.join(''.join(row) for row in unit)
        if key in rules:
            return rules[key]
        unit = rotate(unit)

def rotate(unit: list[list[str]]):
    return list(reversed(list(zip(*unit))))
