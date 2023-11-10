from io import TextIOWrapper

def main(file: TextIOWrapper):
    planet = [[c for c in line.strip()] for line in file.readlines()]
    seen = set()
    encoded = encode(planet)
    while encoded not in seen:
        # for r in planet:
        #     for c in r:
        #         print(c, end='')
        #     print()
        # print()

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
