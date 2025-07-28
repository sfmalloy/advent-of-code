import math
from lib import advent
from io import TextIOWrapper
from collections import deque, defaultdict
from typing import Self


class Program:
    ipt: str
    ip: int
    registers: defaultdict[str, int]
    muls: int    

    def __init__(self, ipt: str):
        self.ipt = ipt
        self.ip = 0
        self.registers = defaultdict(int)
        self.muls = 0

    def step(self):
        if self.registers['a'] == 1 and self.ip+1 == 13:
            return False
        if self.ip < 0 or self.ip >= len(self.ipt):
            return False
        match self.ipt[self.ip]:
            case ('set', x, y):
                self.registers[x] = self.value(y)
            case ('sub', x, y):
                self.registers[x] -= self.value(y)
            case ('mul', x, y):
                self.registers[x] *= self.value(y)
                self.muls += 1
            case ('jnz', x, y):
                if self.value(x) != 0:
                    self.ip += self.value(y) - 1
        self.ip += 1
        return True
    

    def value(self, val: str):
        if val.isalpha():
            return self.registers[val]
        return int(val)



@advent.parser(23)
def parse(file: TextIOWrapper):
    return [line.strip().split() for line in file.readlines()]


@advent.solver(23, part=1)
def solve1(ipt: list[list[str]]):
    prog = Program(ipt)
    while prog.step():
        ...
    return prog.muls


@advent.solver(23, part=2)
def solve2(ipt: list[list[str]]):
    prog = Program(ipt)
    prog.registers['a'] = 1
    while prog.step():
        ...
    lower = prog.registers['b']
    upper = prog.registers['c']

    ans = 0
    for i in range(lower, upper+1, (upper-lower) // 1000):
        if not is_prime(i):
            ans += 1
    return ans


def is_prime(check: int):
    for i in range(2, int(math.sqrt(check))):
        if check % i == 0:
            return False
    return True
