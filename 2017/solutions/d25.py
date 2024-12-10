import re
from lib import advent
from io import TextIOWrapper
from collections import deque, defaultdict
from dataclasses import dataclass

@dataclass
class Rule:
    write: int
    move: int
    next_state: str


@advent.parser(25)
def parse(file: TextIOWrapper):
    start = re.match(r'Begin in state ([A-Z])', file.readline()).groups()[0]
    steps = int(re.search(r'[0-9]+', file.readline())[0])
    rules = defaultdict(list)

    for block in file.read().lstrip().split('\n\n'):
        lines = block.splitlines()
        state = lines[0][-2]
        line_iter = iter(lines)
        line = next(line_iter)

        for _ in range(2):
            line = next(line_iter)
            data = []
            for _ in range(3):
                line = next(line_iter)
                data.append(line.split()[-1][:-1])
            data[0] = int(data[0])
            data[1] = -1 if data[1] == 'left' else 1
            rules[state].append(Rule(*data))

    return start, steps, rules


@advent.solver(25, part=1)
def solve1(state: str, steps: int, rules: defaultdict[str, list[Rule]]):
    memory = defaultdict(int)
    cursor = 0
    for _ in range(steps):
        rule = rules[state][memory[cursor]]
        memory[cursor] = rule.write
        cursor += rule.move
        state = rule.next_state
    return sum(memory.values())


@advent.solver(25, part=2)
def solve2(*args):
    return 'reboot printer'
