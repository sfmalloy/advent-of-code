from io import TextIOWrapper
from collections import defaultdict
from math import ceil


class RecursiveGrid:
    levels: defaultdict[int, list[list[str]]]
    next: defaultdict[int, list[list[str]]]

    def __init__(self, lvl0: list[list[str]]):
        self.levels = defaultdict(lambda: [['.' for _ in range(5)] for _ in range(5)])
        self.next = defaultdict(lambda: [['.' for _ in range(5)] for _ in range(5)])
        self.levels[0] = [[c for c in r] for r in lvl0]

    def __call__(self, lvl: int, r: int, c: int) -> str:
        return self.levels[lvl][r][c]


    def count_neighbor(self, lvl: int, r0: int, c0: int, r1: int, c1: int) -> int:
        rec_dir = 0
        if r1 == -1:
            rec_dir = -1
            r1 = 1
            c1 = 2
        elif r1 == 5:
            rec_dir = -1
            r1 = 3
            c1 = 2
        if c1 == -1:
            rec_dir = -1
            r1 = 2
            c1 = 1
        elif c1 == 5:
            rec_dir = -1
            r1 = 2
            c1 = 3
        
        if r1 == 2 and c1 == 2:
            rec_dir = 1
        
        
        lvl += rec_dir
        if rec_dir != 1:
            return int(self.levels[lvl][r1][c1] == '#')
        
        match r0, c0:
            case 1, 2:
                return sum([int(self.levels[lvl][0][j] == '#') for j in range(5)])
            case 3, 2:
                return sum([int(self.levels[lvl][4][j] == '#') for j in range(5)])
            case 2, 1:
                return sum([int(self.levels[lvl][i][0] == '#') for i in range(5)])
            case 2, 3:
                return sum([int(self.levels[lvl][i][4] == '#') for i in range(5)])


    def count_adjacent(self, lvl: int, r: int, c: int) -> int:
        up = self.count_neighbor(lvl, r, c, r-1, c)
        down = self.count_neighbor(lvl, r, c, r+1, c)
        left = self.count_neighbor(lvl, r, c, r, c-1)
        right = self.count_neighbor(lvl, r, c, r, c+1)
        return up + down + left + right
    

    def step(self):
        self.levels = self.next
        self.next = defaultdict(lambda: [['.' for _ in range(5)] for _ in range(5)])
        assert self.levels != self.next
    
    
    def print(self):
        for lvl, grid in self.levels.items():
            print(f'Level {lvl}')
            for r in grid:
                for c in r:
                    print(c, end='')
                print()
            print()


    def count_bugs(self):
        count = 0
        for grid in self.levels.values():
            for r in grid:
                for c in r:
                    count += c == '#'
        return count


def main(file: TextIOWrapper):
    lines = file.readlines()
    planet = [[c for c in line.strip()] for line in lines]

    seen = set()
    encoded = encode(planet)
    while encoded not in seen:
        seen.add(encoded)
        next_planet = []
        for i,r in enumerate(planet):
            row = []
            for j,c in enumerate(r):
                adj_count = count_adjacent(planet, i, j)
                if c == '#' and adj_count != 1:
                    row.append('.')
                elif c == '.' and (adj_count == 1 or adj_count == 2):
                    row.append('#')
                else:
                    row.append(c)
            next_planet.append(row)
        planet = next_planet
        encoded = encode(planet)

    print(rate(encoded))

    g = RecursiveGrid([[c for c in line.strip()] for line in lines])
    T = 200
    max_lvl = 1
    for t in range(T):
        for lvl in range(-max_lvl, max_lvl+1):
            for r in range(5):
                for c in range(5):
                    if not (r == 2 and c == 2):
                        adj_count = g.count_adjacent(lvl, r, c)
                        if g(lvl, r, c) == '#' and adj_count != 1:
                            g.next[lvl][r][c] = '.'
                        elif g(lvl, r, c) == '.' and (adj_count == 1 or adj_count == 2):
                            g.next[lvl][r][c] = '#'
                        else:
                            g.next[lvl][r][c] = g(lvl, r, c)
        g.step()
        max_lvl = ceil((t+3)/2)
    print(g.count_bugs())


def encode(planet: list[list[str]]):
    tile = 1
    encoded = 0
    for r in planet:
        for c in r:
            encoded |= (c == '#') * tile
            tile <<= 1
    return encoded


def rate(encoded: int):
    tile = 1
    rating = 0
    while tile <= encoded:
        rating += tile * ((tile & encoded) != 0)
        tile <<= 1
    return rating


def count_adjacent(planet: list[list[str]], i: int, j: int):
    up = int(i-1 >= 0 and planet[i-1][j] == '#')
    down = int(i+1 < len(planet) and planet[i+1][j] == '#')
    left = int(j-1 >= 0 and planet[i][j-1] == '#')
    right = int(j+1 < len(planet[i]) and planet[i][j+1] == '#')
    return up + down + left + right
