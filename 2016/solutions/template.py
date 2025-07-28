from io import TextIOWrapper
from dataclasses import dataclass
from collections import deque, defaultdict


def main(file: TextIOWrapper):
    lines = [line.strip() for line in file.readlines()]
    return part1(lines.copy()), part2(lines.copy())


def part1(i):
    return -1


def part2(i):
    return -1
