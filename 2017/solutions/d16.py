from lib import advent
from io import TextIOWrapper
from abc import ABC, abstractmethod


class Move(ABC):
    @abstractmethod
    def move(self, data: list[str]) -> list[str]:
        ...


class Spin(Move):
    size: int

    def __init__(self, m: str):
        self.size = int(m)

    def move(self, data: list[str]) -> list[str]:
        return data[-self.size:] + data[:-self.size]


class Exchange(Move):
    a: int
    b: int

    def __init__(self, m: str):
        self.a, self.b = map(int, m.split('/'))
    
    def move(self, data: list[str]) -> list[str]:
        data[self.a], data[self.b] = data[self.b], data[self.a]
        return data


class Partner(Move):
    p0: int
    p1: int

    def __init__(self, m: str):
        self.p0, self.p1 = m.split('/')

    def move(self, data: list[str]) -> list[str]:
        a = data.index(self.p0)
        b = data.index(self.p1)
        data[a], data[b] = data[b], data[a]
        return data


@advent.parser(16)
def parse(file: TextIOWrapper):
    moves = []
    for move in file.read().strip().split(','):
        match move[0]:
            case 's':
                moves.append(Spin(move[1:]))
            case 'x':
                moves.append(Exchange(move[1:]))
            case 'p':
                moves.append(Partner(move[1:]))
    return moves


@advent.solver(16, part=1)
def solve1(moves: list[Move]):
    data = [chr(c) for c in range(ord('a'), ord('p')+1)]
    return ''.join(dance(moves, data))


@advent.solver(16, part=2, reparse=False)
def solve2(moves: list[tuple[str, str]]):
    seen = []
    data = [chr(c) for c in range(ord('a'), ord('p')+1)]
    i = 0
    # if the cycle didn't happen to be at the start, you could
    # easily modify this to get the index of the cycle start and 
    # modulo by the lenght of the cycle.
    while True:
        order = ''.join(data)
        if seen and order == seen[0]:
            break
        seen.append(order)
        i += 1
        data = dance(moves, data)
    return seen[1_000_000_000 % len(seen)]


def dance(moves: list[Move], data: list[str]) -> list[str]:
    for m in moves:
        data = m.move(data)
    return data

