import re
from io import TextIOWrapper
from dataclasses import dataclass

@dataclass(frozen=True, eq=True)
class Node:
    x: int
    y: int
    size: int
    used: int
    avail: int
    used_percent: int


def main(file: TextIOWrapper):
    lines = [line.strip() for line in file.readlines()]
    nodes = dict()
    for line in lines[2:]:
        node = Node(*map(int, re.findall(r'\d+', line)))
        nodes[node.x, node.y] = node
    return part1(nodes), None


def part1(nodes: dict[tuple[int, int], Node]):
    pairs = set()
    for a in nodes.values():
        if not a.used:
            continue
        for b in nodes.values():
            if a == b:
                continue
            if a.used <= b.avail:
                pairs.add((a, b))
    return len(pairs)


def part2(i):
    return -1
