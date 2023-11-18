from .lib.advent import advent
from io import TextIOWrapper


@advent.parser(11)
def parse(file: TextIOWrapper):
    return file.read().strip().split(',')


@advent.day(11)
def solve1(dirs: list[str]):
    r = 0
    c = 0
    far = 0
    for d in dirs:
        match d:
            case 'n':
                r -= 2
            case 'ne':
                r -= 1
                c += 1
            case 'se':
                r += 1
                c += 1
            case 's':
                r += 2
            case 'sw':
                r += 1
                c -= 1
            case 'nw':
                r -= 1
                c -= 1
        far = max(far, dist(r,c))
    return dist(r, c), far


def dist(r: int, c: int):
    return (abs(r) + abs(c))//2
