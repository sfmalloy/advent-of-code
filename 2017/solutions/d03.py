from lib import advent
from io import TextIOWrapper
from collections import deque


@advent.parser(3)
def parse(file: TextIOWrapper) -> int:
    return int(file.read().strip())


@advent.solver(3, part=1)
def solve1(goal: int):
    n = f = 0
    while f < goal:
        f = (2*n+1)**2
        n += 1
    n -= 1
    return min(abs((f-x*n)-goal)+n for x in range(1,8,2))


@advent.solver(3, part=2)
def solve2(goal: int):
    grid = deque([deque([1])])
    # extra grow at the beginning to leave a buffer of 0s
    # makes writing spiral sum code WAY EASIER because you can
    # effectively ignore bounds checking
    grow(grid)
    
    while True:
        grow(grid)
        r = 1
        c = 2
        while c < len(grid)-2:
            grid[r][c] = spiral_sum(grid, r, c)
            if grid[r][c] > goal:
                return grid[r][c]
            c += 1
        while r < len(grid)-2:
            grid[r][c] = spiral_sum(grid, r, c)
            if grid[r][c] > goal:
                return grid[r][c]
            r += 1
        while c > 1:
            grid[r][c] = spiral_sum(grid, r, c)
            if grid[r][c] > goal:
                return grid[r][c]            
            c -= 1
        while r > 1:
            grid[r][c] = spiral_sum(grid, r, c)
            if grid[r][c] > goal:
                return grid[r][c]
            r -= 1
        while c < 2:
            grid[r][c] = spiral_sum(grid, r, c)
            if grid[r][c] > goal:
                return grid[r][c]
            c += 1


def grow(grid: deque[deque[int]]):
    for row in grid:
        row.append(0)
        row.appendleft(0)
    L = len(grid[0])
    grid.appendleft(deque([0 for _ in range(L)]))
    grid.append(deque([0 for _ in range(L)]))


def spiral_sum(grid: deque[deque[int]], r: int, c: int) -> int:
    top = grid[r-1][c-1] + grid[r-1][c] + grid[r-1][c+1]
    middle = grid[r][c-1] + grid[r][c] + grid[r][c+1]
    bottom = grid[r+1][c-1] + grid[r+1][c] + grid[r+1][c+1]
    return top+middle+bottom
