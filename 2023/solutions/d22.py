from collections import defaultdict
from dataclasses import dataclass, field
from io import TextIOWrapper

from .lib.advent import advent
from .lib.util import Vec3


@dataclass
class CubeData:
    bricks: defaultdict[int, set[Vec3]] = field(default_factory=defaultdict(set))
    plane: defaultdict[Vec3, int] = field(default_factory=defaultdict(int))


@advent.parser(22)
def parse(file: TextIOWrapper):
    lines = [line.strip() for line in file.readlines()]
    bricks = defaultdict(set)
    plane = defaultdict(int)
    for i, line in enumerate(lines):
        start, end = line.split('~')
        start_cube = Vec3(*map(int, start.split(',')))
        end_cube = Vec3(*map(int, end.split(',')))
        brick = set()
        for x in range(start_cube.x, end_cube.x + 1):
            for y in range(start_cube.y, end_cube.y + 1):
                for z in range(start_cube.z, end_cube.z + 1):
                    brick.add(Vec3(x, y, z))
                    plane[Vec3(x, y, z)] = i
        bricks[i] = brick
    return CubeData(bricks, plane)


@advent.day(22, part=1)
def solve1(data: CubeData):
    data = fall(data)

    answer = len(data.bricks)
    for b, brick in data.bricks.items():
        tmp = CubeData(data.bricks.copy(), data.plane.copy())
        disintegrate(b, brick, tmp)
        safe = fall(tmp, True)
        if not safe:
            answer -= 1

    return answer


@advent.day(22, part=2)
def solve2(ipt):
    return 0


def fall(data: CubeData, validate: bool = False):
    while True:
        floating_cubes = defaultdict(set)
        for cube, i in data.plane.items():
            floaty = cube - Vec3(0, 0, 1)
            if cube.z > 0 and (floaty not in data.plane or data.plane.get(floaty) == i):
                floating_cubes[i].add(cube)

        found = False
        new_data = CubeData(data.bricks.copy(), data.plane.copy())
        for i, cube in floating_cubes.items():
            if data.bricks[i] == cube:
                if validate:
                    return False
                found = True
                lowered = set()
                for vec in cube:
                    v = vec - Vec3(0, 0, 1)
                    lowered.add(v)
                for vec in cube:
                    if vec not in lowered:
                        del new_data.plane[vec]
                for vec in lowered:
                    new_data.plane[vec] = i
                new_data.bricks[i] = lowered
        data = new_data
        if not found:
            return data


def disintegrate(i: int, brick: set[Vec3], data: CubeData):
    for b in brick:
        del data.plane[b]
    del data.bricks[i]
    return data
