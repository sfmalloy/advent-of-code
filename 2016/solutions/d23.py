import re
import math
from io import TextIOWrapper


def main(file: TextIOWrapper):
    lines = [line.strip() for line in file.readlines()]
    return run(lines, 7), run(lines, 12)


def run(program: list[str], init: int):
    nums = set()
    for line in program:
        line_nums = re.findall(r'-?\d+', line)
        nums |= set(map(int, line_nums))
    c = nums.remove(max(nums))
    d = nums.remove(max(nums))
    return math.factorial(init) + c*d
