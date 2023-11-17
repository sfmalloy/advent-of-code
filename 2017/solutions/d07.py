import re
from .lib.advent import advent
from io import TextIOWrapper
from typing import Self, Optional
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Program:
    name: str
    weight: int
    above: Optional[list[Self]]=None


@advent.parser(7)
def parse(file: TextIOWrapper) -> dict[str, Program]:
    programs: dict[str, Program] = {}
    for line in file.readlines():
        struct = line.strip().split(' -> ')
        name, weight = re.search(r'([a-z]+) \((\d+)\)', struct[0]).groups()
        programs[name] = Program(name, int(weight))
        if len(struct) == 2:
            programs[name].above = struct[1].split(', ')
    return programs


@advent.day(7, part=1)
def solve1(programs: dict[str, Program]):
    bottom = ''
    for prog in programs:
        stack = [prog]
        seen = set()
        while len(stack) > 0:
            name = stack.pop()
            seen.add(name)
            curr = programs[name]
            if curr.above:
                for child in curr.above:
                    if child not in seen:
                        stack.append(child)
        if len(seen) == len(programs):
            bottom = prog
            break
    return bottom


@advent.day(7, part=2, use_part1=True)
def solve2(programs: dict[str, Program], bottom: str):
    weights: defaultdict[list[str]] = defaultdict(list)
    diff = 0
    while True:
        for child in programs[bottom].above:
            weight = total_weight(programs[child], programs)
            weights[weight].append(child)
        for weight, names in weights.items():
            if len(names) == 1:
                nums = list(weights.keys())
                diff = max(nums) - min(nums)
                bottom = names[0]
        if not programs[bottom].above or len(weights) == 1:
            return programs[bottom].weight - diff
        weights = defaultdict(list)


def total_weight(parent: Program, programs: dict[Program]):
    if not parent.above:
        return parent.weight
    total = parent.weight
    for child in parent.above:
        total += total_weight(programs[child], programs)
    return total
