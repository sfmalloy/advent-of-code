from lib import advent
from io import TextIOWrapper
from collections import deque, defaultdict
from dataclasses import dataclass, field

@dataclass(frozen=True, eq=True)
class Port:
    a: int
    b: int
    a_used: bool = field(default=False, compare=False)
    b_used: bool = field(default=False, compare=False)

    def copy(self, a_used: bool, b_used: bool):
        return Port(self.a, self.b, a_used, b_used)

    def strength(self):
        return self.a + self.b


@advent.parser(24)
def parse(file: TextIOWrapper):
    return [Port(*map(int, line.strip().split('/'))) for line in file.readlines()]


@advent.solver(24)
def solve1(ports: list[Port]):
    q: deque[list[Port]] = deque([])
    for p in ports:
        if p.a == 0:
            q.append([p.copy(True, False)])
        if p.b == 0:
            q.append([p.copy(False, True)])
    
    p1 = 0
    p2 = (0, 0)
    while q:
        curr = q.popleft()
        s = sum(p.strength() for p in curr)
        if s > p1:
            p1 = s
        if len(curr) > p2[0]:
            p2 = (len(curr), s)
        elif len(curr) == p2[0]:
            p2 = (p2[0], max(s, p2[1]))
        for p in ports:
            if p not in curr:
                if not curr[-1].a_used:
                    if p.a == curr[-1].a:
                        q.append(curr + [p.copy(True, False)])
                    elif p.b == curr[-1].a:
                        q.append(curr + [p.copy(False, True)])
                if not curr[-1].b_used:
                    if p.a == curr[-1].b:
                        q.append(curr + [p.copy(True, False)])
                    elif p.b == curr[-1].b:
                        q.append(curr + [p.copy(False, True)])
    return p1, p2[1]
