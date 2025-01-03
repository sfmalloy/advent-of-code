from io import TextIOWrapper
from dataclasses import dataclass
from collections import deque, defaultdict


def main(file: TextIOWrapper):
    lines = [line.strip() for line in file.readlines()]
    return part1(lines.copy()), part2(lines.copy())


def part1(prog: list[str]):
    word = deque('abcdefgh')
    for line in prog:
        match line.split():
            case ['swap', 'position', x, 'with', 'position', y]:
                a = int(x)
                b = int(y)
                word[a], word[b] = word[b], word[a]
            case ['swap', 'letter', x, 'with', 'letter', y]:
                a = word.index(x)
                b = word.index(y)
                word[a], word[b] = word[b], word[a]
            case ['rotate', d, x, 'step' | 'steps']:
                a = int(x)
                word.rotate(a if d == 'right' else -a)
            case ['rotate', 'based', 'on', 'position', 'of', 'letter', x]:
                a = word.index(x)
                word.rotate(1 + a)
                if a >= 4:
                    word.rotate(1)
            case ['reverse', 'positions', x, 'through', y]:
                a = int(x)
                b = int(y)
                for i, c in enumerate(reversed([word[i] for i in range(a, b+1)]), start=a):
                    word[i] = c
            case ['move', 'position', x, 'to', 'position', y]:
                a = int(x)
                b = int(y)
                v = word[a]
                word.remove(v)
                word.insert(b, v)
    return ''.join(word)



def part2(prog: list[str]):
    word = deque('fbgdceah')
    for line in reversed(prog):
        match line.split():
            case ['swap', 'position', x, 'with', 'position', y]:
                a = int(x)
                b = int(y)
                word[a], word[b] = word[b], word[a]
            case ['swap', 'letter', x, 'with', 'letter', y]:
                a = word.index(x)
                b = word.index(y)
                word[a], word[b] = word[b], word[a]
            case ['rotate', d, x, 'step' | 'steps']:
                a = int(x)
                word.rotate(a if d == 'left' else -a)
            case ['rotate', 'based', 'on', 'position', 'of', 'letter', x]:
                a = word.index(x)
                match a:
                    case 1: i = 1
                    case 3: i = 2
                    case 5: i = 3
                    case 7: i = 4
                    case 0: i = 1
                    case 2: i = 6
                    case 4: i = 7
                    case 6: i = 8
                word.rotate(-i)
            case ['reverse', 'positions', x, 'through', y]:
                a = int(x)
                b = int(y)
                for i, c in enumerate(reversed([word[i] for i in range(a, b+1)]), start=a):
                    word[i] = c
            case ['move', 'position', x, 'to', 'position', y]:
                a = int(y)
                b = int(x)
                v = word[a]
                word.remove(v)
                word.insert(b, v)
    return ''.join(word)
