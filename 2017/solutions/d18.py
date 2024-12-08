from lib import advent
from io import TextIOWrapper
from collections import defaultdict, deque
from typing import Self


class Program:
    ipt: str
    name: str
    ip: int
    q: deque[int]
    registers: defaultdict[str, int]
    waiting: bool
    sends: int

    def __init__(self, ipt: str, id: int):
        self.ipt = ipt
        self.name = 'a' if id == 0 else 'b'
        self.ip = 0
        self.q = deque()
        self.registers = defaultdict(int)
        self.registers['p'] = id
        self.waiting = False
        self.sends = 0


    def step(self, other: Self):
        if self.ip < 0 or self.ip >= len(self.ipt):
            print('forever waiting')
            self.waiting = True
            return
        match self.ipt[self.ip]:
            case ('snd', x):
                self.sends += 1
                other.q.append(self.value(x))
            case ('set', x, y):
                self.registers[x] = self.value(y)
            case ('add', x, y):
                self.registers[x] += self.value(y)
            case ('mul', x, y):
                self.registers[x] *= self.value(y)
            case ('mod', x, y):
                self.registers[x] %= self.value(y)
            case ('rcv', x):
                if not self.q:
                    self.waiting = True
                    return
                else:
                    self.registers[x] = self.q.popleft()
                    self.waiting = False
            case ('jgz', x, y):
                if self.value(x) > 0:
                    self.ip += self.value(y) - 1
        self.ip += 1
    
    def value(self, val: str):
        if val.isalpha():
            return self.registers[val]
        return int(val)


@advent.parser(18)
def parse(file: TextIOWrapper):
    return [tuple(line.strip().split()) for line in file.readlines()]


@advent.solver(18, part=1)
def solve1(ipt: list[tuple]):
    a = Program(ipt, 0)
    b = Program('', 0)
    while not a.waiting:
        a.step(b)
    return b.q[-1]


@advent.solver(18, part=2)
def solve2(ipt: list[tuple]):
    a = Program(ipt, 0)
    b = Program(ipt, 1)
    while not (a.waiting and b.waiting):
        a.step(b)
        b.step(a)
    return b.sends
