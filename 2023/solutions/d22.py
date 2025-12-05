from .lib.advent import advent
from .lib.util import Vec3
from io import TextIOWrapper
from dataclasses import dataclass, field
from io import TextIOWrapper

from .lib.advent import advent
from .lib.util import Vec3


@dataclass
class Brick:
    cubes: set[Vec3] = field(default_factory=set)

    def fall(self, space: set[Vec3], *, do_update: bool = True):
        fallen = set()
        for cube in self.cubes:
            down = cube - Vec3(0, 0, 1)
            if cube.z == 0 or (down in space and down not in self.cubes):
                return False
            fallen.add(down)
        if do_update:
            space.difference_update(self.cubes)
            self.cubes = fallen
            space.update(self.cubes)
        return True


@dataclass
class Data:
    bricks: list[Brick]
    space: set[Vec3]


@advent.parser(22)
def parse(file: TextIOWrapper):
    space = set()
    bricks = []
    for line in file:
        v0, v1 = map(lambda t: Vec3(*[int(t) for t in t.split(",")]), line.split("~"))
        brickset = set()
        for x in range(min(v0.x, v1.x), max(v0.x, v1.x) + 1):
            for y in range(min(v0.y, v1.y), max(v0.y, v1.y) + 1):
                for z in range(min(v0.z, v1.z), max(v0.z, v1.z) + 1):
                    vec = Vec3(x, y, z)
                    brickset.add(vec)
                    space.add(vec)
        bricks.append(Brick(brickset))
    return Data(bricks=bricks, space=space)


@advent.day(22, part=1)
def solve1(data: Data):
    while True:
        updated = 0
        any_fell = False
        for brick in data.bricks:
            fell = brick.fall(data.space)
            if fell:
                updated += 1
            any_fell = any_fell or fell
        if not any_fell:
            break

    safe = len(data.bricks)
    for brick in data.bricks:
        data.space -= brick.cubes
        for inner in data.bricks:
            if inner.fall(data.space, do_update=False):
                safe -= 1
                break
        data.space |= brick.cubes
    return safe


@advent.day(22, part=2)
def solve2(ipt):
    return 0
