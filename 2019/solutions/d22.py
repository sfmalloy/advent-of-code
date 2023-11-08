from io import TextIOWrapper
from typing import Self, Optional
from dataclasses import dataclass


def main(file: TextIOWrapper):
    commands = file.readlines()
    print(part1(commands, 10007, 2019))


def part1(commands: list[str], N: int, pos: int):
    for cmd in commands:
        words = cmd.split()
        match words:
            case ['cut', x]:
                pos = cut(pos, int(x), N)
            case ['deal', 'into', 'new', 'stack']:
                pos = new_stack(pos, N)
            case ['deal', 'with', 'increment', x]:
                pos = deal(pos, int(x), N)
        print(words, pos)
    return pos


def new_stack(pos: int, N: int) -> int:
    return -(pos + 1) % N


def cut(pos: int, x: int, N: int) -> int:
    if x < 0:
        x += N
    return (pos + (N - x)) % N


def deal(pos: int, x: int, N: int) -> int:
    return (x * pos) % N
