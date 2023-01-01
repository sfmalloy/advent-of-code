import re
from io import TextIOWrapper
from dataclasses import dataclass
from functools import reduce


@dataclass
class Disc:
    total: int
    pos: int

    def rotate(self):
        self.pos += 1
        self.pos %= self.total


def get_capsule(starting_discs: list[Disc]):
    num_cycles = reduce(lambda total, curr: total * curr.total, starting_discs, 1)

    discs = [Disc(disc.total, disc.pos) for disc in starting_discs]
    for c in range(num_cycles):
        positions = []
        for d in discs:
            d.rotate()
            positions.append(d.pos)
        found = True
        for i,p in enumerate(positions):
            if p != (discs[i].total - (i+1)) % discs[i].total:
                found = False
        if found:
            return c+1
    return -1

def main(file: TextIOWrapper):
    discs: list[Disc] = []
    num_cycles = 1
    for line in file.readlines():
        _, total, _, start = map(int, re.findall('\d+', line))
        discs.append(Disc(total, start))
        num_cycles *= total
    
    p1 = get_capsule(discs)
    p2 = get_capsule(discs+[Disc(11, 0)])

    return p1,p2
