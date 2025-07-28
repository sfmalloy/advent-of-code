from io import TextIOWrapper
from collections import deque


def main(file: TextIOWrapper):
    grid = [line.strip() for line in file.readlines()]
    dirs = [
        0+1j,
        1+0j,
        0-1j,
        -1+0j
    ]
    start = find_start(grid)
    q = deque([(start, [], 0)])
    visited = set()
    p1 = 0
    while q:
        curr, found, steps = q.popleft()
        r = row(curr)
        c = col(curr)
        if (curr, ''.join(found)) in visited:
            continue
        if grid[r][c].isdigit() and int(grid[r][c]) > 0:
            found = found + [grid[r][c]]
        if len(set(found)) == 7:
            end = complex(c, r)
            p1 = steps
            break
        visited.add((curr, ''.join(found)))
        for d in dirs:
            new = curr + d
            if grid[row(new)][col(new)] != '#':
                q.append((new, found, steps + 1))
    
    q = deque([(end, 0)])
    p2 = 0
    while q:
        curr, steps = q.popleft()
        r = row(curr)
        c = col(curr)
        if curr in visited:
            continue
        if curr == start:
            p2 = steps
            break
        visited.add(curr)
        for d in dirs:
            new = curr + d
            if grid[row(new)][col(new)] != '#':
                q.append((new, steps + 1))

    return p1, p1+p2


def find_start(grid: list[str]):
    for r, rw in enumerate(grid):
        if (c := rw.find('0')) != -1:
            return complex(c, r)


def col(n: complex) -> int:
    return int(n.real)


def row(n: complex) -> int:
    return int(n.imag)
