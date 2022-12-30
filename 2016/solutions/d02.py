from io import TextIOWrapper
from dataclasses import dataclass
from typing import Self


@dataclass
class Point:
    r: int = 0
    c: int = 0

    def step(self, other: Self, keypad: list[list[str]]) -> Self:
        if self.r+other.r >= 0 and self.r+other.r < len(keypad) and self.c+other.c >= 0 and self.c+other.c < len(keypad[self.r+other.r]):
            if keypad[self.r+other.r][self.c+other.c] != '.':
                self.r += other.r
                self.c += other.c


dirs = {
    'U': Point(-1, 0),
    'R': Point(0, 1),
    'D': Point(1, 0),
    'L': Point(0, -1)
}

def walk(steps, keypad):
    digits = ''
    curr = Point()
    while '5' not in keypad[curr.r]:
        curr.r += 1
    curr.c = keypad[curr.r].index('5')
    print(curr)
    for line in steps:
        steps = line.strip()
        for step in steps:
            curr.step(dirs[step], keypad)
        digits += keypad[curr.r][curr.c]
    return digits


def main(file: TextIOWrapper):
    steps = file.readlines()
    p1 = walk(steps, [
        '123',
        '456',
        '789'
    ])

    p2 = walk(steps, [
        '..1..',
        '.234.',
        '56789',
        '.ABC.',
        '..D..'
    ])

    return p1,p2
