from io import TextIOWrapper
from collections import defaultdict

def main(in_file: TextIOWrapper):
    grid = [line.strip() for line in in_file.readlines()]

    portals = defaultdict(set)
    for r in range(len(grid)-1):
        for c in range(1, len(grid[r])-1):
            if grid[r][c].isalpha():
                if grid[r][c-1].isalpha():
                    portals[grid[r][c-1]+grid[r][c]].add((r,c))
                elif grid[r][c+1].isalpha():
                    portals[grid[r][c]+grid[r][c+1]].add((r,c))
                elif grid[r+1][c].isalpha():
                    portals[grid[r][c]+grid[r+1][c]].add((r,c))
    print(portals)
