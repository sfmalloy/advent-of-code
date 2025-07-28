from io import TextIOWrapper
from collections import defaultdict, deque
from dataclasses import dataclass, field


@dataclass
class Portal:
    r1: int
    c1: int
    r2: int = -1
    c2: int = -1


@dataclass
class Node:
    r: int
    c: int
    dist: int
    level: int = 0
    path: list = field(default_factory=lambda: [])


# north, east, south, west
DR = [-1,0,1,0]
DC = [0,1,0,-1]

def find_path_non_recursive(grid: list[list[str]], portals: dict[str, Portal]):
    q = deque([Node(portals['AA'].r1, portals['AA'].c1, 0)])
    visited = set()
    while len(q) > 0:
        curr = q.popleft()
        if curr.r == portals['ZZ'].r1 and curr.c == portals['ZZ'].c1:
            return curr.dist
        visited.add((curr.r, curr.c))
        
        for dr, dc in zip(DR, DC):
            new_r = curr.r+dr
            new_c = curr.c+dc
            if new_r < len(grid) and new_r >= 0 and new_c < len(grid[curr.r]) and new_c >= 0 and (new_r, new_c) not in visited:
                elem = grid[new_r][new_c]
                if elem == '.' or elem == 'ZZ':
                    q.append(Node(new_r, new_c, curr.dist+1))
                elif elem != '#':
                    portal = portals[elem]
                    if new_r == portal.r1 and new_c == portal.c1:
                        new_r = portal.r2
                        new_c = portal.c2
                    else:
                        new_r = portal.r1
                        new_c = portal.c1
                    q.append(Node(new_r, new_c, curr.dist+2))


def find_path_recursive(grid: list[list[str]], portals: dict[str, Portal]):
    q = deque([Node(portals['AA'].r1, portals['AA'].c1, 0)])
    visited = set()
    while len(q) > 0:
        curr = q.popleft()
        if curr.r == portals['ZZ'].r1 and curr.c == portals['ZZ'].c1 and curr.level == 0:
            print(curr.path)
            return curr.dist
        visited.add((curr.r, curr.c, curr.level))

        for dr, dc in zip(DR, DC):
            new_r = curr.r+dr
            new_c = curr.c+dc
            if new_r < len(grid) and new_r >= 0 and new_c < len(grid[curr.r]) and new_c >= 0 and (new_r, new_c, curr.level) not in visited:
                elem = grid[new_r][new_c]
                if elem == '.' or elem == 'ZZ':
                    q.append(Node(new_r, new_c, curr.dist+1, curr.level, curr.path))
                elif elem != '#':
                    portal = portals[elem]
                    dl = -1 if (new_r == 2 or new_c == 2 or new_r == len(grid)-3 or new_c == len(grid[0])-3) else 1
                    if new_r == portal.r1 and new_c == portal.c1:
                        new_r = portal.r2
                        new_c = portal.c2
                    else:
                        new_r = portal.r1
                        new_c = portal.c1
                    if (dl == -1 and curr.level != 0) or dl == 1:
                        # print(elem, dl, curr.level)
                        q.append(Node(new_r, new_c, curr.dist+2, curr.level+dl, curr.path + [(elem, curr.level+dl)]))



def main(file: TextIOWrapper):
    ipt: list[str] = [line.strip('\n') for line in file.readlines()]

    portal_lists = defaultdict(list)
    grid = []
    # portal parsing is going to be "fun"
    for r, line in enumerate(ipt):
        row = []
        for c, symbol in enumerate(line):
            if symbol.isalpha():
                if r+1 < len(ipt) and ipt[r+1][c].isalpha():
                    name = f'{symbol}{ipt[r+1][c]}'
                    if r-1 > 0 and ipt[r-1][c] == '.':
                        portal_lists[name].append(Portal(r-1,c))
                    else:
                        portal_lists[name].append(Portal(r+2,c))
                elif c+1 < len(ipt[r]) and ipt[r][c+1].isalpha():
                    name = f'{symbol}{ipt[r][c+1]}'
                    if c-1 > 0 and ipt[r][c-1] == '.':
                        portal_lists[name].append(Portal(r,c-1))
                    else:
                        portal_lists[name].append(Portal(r,c+2))
                row.append('#')
            elif symbol == '#' or symbol == ' ':
                row.append('#')
            else:
                row.append('.')
        grid.append(row)
    

    portals: dict[str, Portal] = {}
    for name,lst in portal_lists.items():
        if len(lst) == 2:
            portals[name] = Portal(lst[0].r1,lst[0].c1, lst[1].r1,lst[1].c1)
            grid[lst[0].r1][lst[0].c1] = name
            grid[lst[1].r1][lst[1].c1] = name
        else:
            portals[name] = lst[0]
            grid[lst[0].r1][lst[0].c1] = name
    
    print(find_path_non_recursive(grid, portals))
    print(find_path_recursive(grid, portals))
