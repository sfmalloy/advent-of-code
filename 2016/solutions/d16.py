from io import TextIOWrapper
from collections import deque


def step(start: str):
    a = deque(start)
    b = deque()
    for bit in a:
        b.appendleft('0' if bit == '1' else '1')
    a.append('0')
    return ''.join(a+b)


def checksum(data: str):
    res = ''
    while len(data) % 2 == 0:
        res = ''
        for i in range(0, len(data), 2):
            res += '1' if data[i] == data[i+1] else '0'
        data = res
    return res


def fill_disk(size: int, start: str):
    curr = start
    while len(curr) < size:
        curr = step(curr)
    curr = curr[:size]
    return checksum(curr)


def main(file: TextIOWrapper):
    data = file.read().strip()
    return fill_disk(272, data), fill_disk(35651584, data)
