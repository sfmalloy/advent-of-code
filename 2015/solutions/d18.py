from io import TextIOWrapper

def adj_count(mr, mc, grid):
    count = 0
    for r in range(mr-1, mr+2):
        if r < len(grid) and r >= 0:
            for c in range(mc-1, mc+2):
                if c < len(grid[r]) and c >= 0 and not (r == mr and c == mc):
                    count += int(grid[r][c])
    return count

def new_grid(grid, part2=False):
    new = []
    for r, row in enumerate(grid):
        new_row = []
        for c, col in enumerate(row):
            count = adj_count(r, c, grid)
            new_row.append((col and (count == 2 or count == 3)) or (not col and count == 3))
        new.append(new_row)
    if part2:
        new[0][0] = new[0][-1] = new[-1][0] = new[-1][-1] = True
    return new

def main(in_file: TextIOWrapper):
    grid1 = [[c == '#' for c in r.strip()] for r in in_file.readlines()]
    grid2 = [[c for c in r] for r in grid1]
    steps = 100
    for _ in range(steps):
        grid1 = new_grid(grid1)
        grid2 = new_grid(grid2, True)
    print(sum([sum(r) for r in grid1]))
    print(sum([sum(r) for r in grid2]))
