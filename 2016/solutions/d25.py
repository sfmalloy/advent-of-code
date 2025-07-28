from io import TextIOWrapper
from .assembunny import Assembunny


def main(file: TextIOWrapper):
    lines = [line.strip() for line in file.readlines()]
    return part1(lines.copy()), 'Merry Christmas!'


def part1(lines: list[str]):
    a = 0
    while True:
        comp = Assembunny(lines, [a, 0, 0, 0])
        output = []
        while True:
            out = comp.run()
            if out is None:
                break
            else:
                output.append(out)
                if comp.mem[0] == 0:
                    break
        valid = True
        on = False
        for o in output:
            if (on and not o) or (not on and o):
                valid = False
            on = not on
        if valid:
            return a
        a += 1
