from .lib.advent import advent
from io import TextIOWrapper


@advent.parser(6)
def parse(file: TextIOWrapper):
    return list(map(int, file.read().split('\t')))


@advent.day(6)
def solve(mem: list[int]):
    seen = {}
    N = len(mem)
    count = 0
    while tuple(mem) not in seen:
        seen[tuple(mem)] = count
        start = max_index(mem)
        dist = mem[start]
        mem[start] = 0
        distrib = [0 for _ in range(N)]
        for i,amt_i in zip(range(start+1, start+N+1), range(0, min(N,dist))):
            i %= N
            delta = partition(dist, amt_i+1, min(N, dist))-partition(dist, amt_i, min(N, dist))
            distrib[i] = delta
            mem[i] += delta
        count += 1
    return count, count-seen[tuple(mem)]


def max_index(mem: list[int]) -> int:
    mx = 0
    idx = 0
    for i,elem in enumerate(mem):
        if mx < elem:
            idx = i
            mx = elem
    return idx


def partition(amt: int, idx: int, N: int) -> int:
    return idx*amt // N
