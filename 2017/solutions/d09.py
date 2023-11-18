from .lib.advent import advent
from io import TextIOWrapper


@advent.parser(9)
def parse(file: TextIOWrapper):
    return file.read().strip()


@advent.day(9)
def solve(stream: str):
    score = 0
    garbage = 0
    group = 0
    in_garbage = False
    i = 0
    while i < len(stream):
        if stream[i] == '!':
            i += 1
        elif in_garbage:
            if stream[i] == '>':
                in_garbage = False
            else:
                garbage += 1
        else:
            if stream[i] == '<':
                in_garbage = True
            elif stream[i] == '{':
                group += 1
            elif stream[i] == '}':
                score += group
                group -= 1
        i += 1
    return score, garbage

