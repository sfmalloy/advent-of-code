from lib import advent
from io import TextIOWrapper
from dataclasses import dataclass, field


@dataclass
class Program:
    id: int
    children: list[int] = field(default_factory=lambda: [])


@advent.parser(12)
def parse(file: TextIOWrapper) -> list[Program]:
    programs: list[Program] = []
    for line in file.readlines():
        prog_id, children = line.split(' <-> ')
        programs.append(Program(int(prog_id), list(map(int, children.split(', ')))))
    return programs


@advent.solver(12, part=1)
def solve1(programs: list[Program]):
    root = 0
    found = 0
    for p in programs:
        found += is_connected(root, p.id, frozenset(), programs)
    return found


@advent.solver(12, part=2)
def solve2(programs: list[Program]):
    visited = set()
    groups = 0
    i = 0
    while len(visited) < len(programs):
        groups += 1
        visited |= visit_all(i, frozenset([i]), programs)
        while i in visited:
            i += 1
    return groups


def is_connected(goal: int, prev: int, seen: frozenset[int], programs: list[Program]):
    if prev == goal:
        return True
    for p in programs[prev].children:
        if p not in seen:
            found = is_connected(goal, p, seen | {p}, programs)
            if found:
                return True
    return False


def visit_all(prev: int, seen: frozenset[int], programs: list[Program]):
    for p in programs[prev].children:
        if p not in seen:
            seen |= visit_all(p, seen | {p}, programs)
    return seen
