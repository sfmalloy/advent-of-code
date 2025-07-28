from io import TextIOWrapper
from itertools import pairwise
from collections import deque


def main(file: TextIOWrapper):
    ranges = sorted([tuple(map(int, line.strip().split('-'))) for line in file.readlines()])
    ranges.sort()
    q_out = deque(ranges)
    q_in = deque()
    while q_out:
        q_in.append(q_out.popleft())
        a, b = q_in[-1]
        if not q_out:
            break
        if b >= q_out[0][0]:
            if b < q_out[0][1]:
                b = q_out[0][0]-1
            else:
                q_out.popleft()
                q_out.appendleft(q_in.pop())

    p1 = None
    p2 = 0
    for a, b in pairwise(q_in):
        if not a or not b:
            continue
        if b[0] - a[1] > 1:
            if p1 is None:
                p1 = a[1] + 1
            p2 += b[0] - a[1] - 1
    return p1, p2
