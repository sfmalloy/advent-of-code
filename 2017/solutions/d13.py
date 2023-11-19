from .lib.advent import advent
from io import TextIOWrapper


class Layer:
    depth: int
    scanner_pos: int
    dir: int
    cycle: int

    def __init__(self, depth):
        self.depth = depth
        self.scanner_pos = 0
        self.dir = 1
        self.cycle = 2*(self.depth - 1)


    def step(self):
        if self.depth == 0:
            return
        self.scanner_pos += self.dir
        if self.scanner_pos == self.depth-1 or self.scanner_pos == 0:
            self.dir *= -1


@advent.parser(13)
def parse(file: TextIOWrapper) -> list[Layer]:
    layers: list[Layer] = []
    for line in file.readlines():
        lid, depth = map(int, line.split(': '))
        while lid != len(layers):
            layers.append(Layer(0))
        layers.append(Layer(depth))
    return layers


@advent.day(13, part=1)
def solve1(layers: list[Layer]):
    time = 0
    severity = 0
    while time < len(layers):
        if layers[time].depth > 0 and layers[time].scanner_pos == 0:
            severity += time * layers[time].depth
        for l in layers:
            l.step()
        time += 1
    return severity


@advent.day(13, part=2)
def solve2(layers: list[Layer]):
    delay = 0
    found = False
    while not found:
        found = True
        for lid,l in enumerate(layers):
            if l.depth != 0 and (delay+lid) % l.cycle == 0:
                found = False
                break
        delay += 1
    return delay-1
