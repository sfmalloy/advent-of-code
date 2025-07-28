from io import TextIOWrapper
from dataclasses import dataclass
from typing import Self


@dataclass
class Point:
    r: int = 0
    c: int = 0
    dir: int = 0

    def __add__(self, other: Self) -> Self:
        return Point(self.r+other.r, self.c+other.c, self.dir)

    def mdist(self, other: Self) -> int:
        return abs(self.r-other.r) + abs(self.c-other.c)


def main(file: TextIOWrapper):
    dirs = [
        Point(-1, 0),
        Point(0, 1),
        Point(1, 0),
        Point(0, -1),
    ]
    me = Point()
    points = set()
    p2 = None
    for step in file.read().strip().split(', '):
        turn = step[0]
        dist = int(step[1:])
        me.dir = (me.dir + (1 if turn == 'R' else -1)) % 4
        for _ in range(dist):
            me += dirs[me.dir]
            if p2 is None and (me.r, me.c) in points:
                p2 = me.mdist(Point(0, 0))
            points.add((me.r, me.c))
    p1 = me.mdist(Point(0, 0))


    return p1,p2
