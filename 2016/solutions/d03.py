from io import TextIOWrapper


def main(file: TextIOWrapper):
    p1 = 0
    lines = [list(map(int, line.split())) for line in file.readlines()]
    for line in lines:
        sides = sorted(line)
        p1 += sides[0] + sides[1] > sides[2]

    p2 = 0
    for r in range(0, len(lines), 3):
        for c in range(3):
            group = sorted([lines[r][c], lines[r+1][c], lines[r+2][c]])
            p2 += group[0] + group[1] > group[2]

    return p1,p2
