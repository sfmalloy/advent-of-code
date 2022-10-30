from collections import defaultdict
from dataclasses import dataclass
from io import TextIOWrapper

@dataclass
class Node:
    src: str
    neighbor: str
    del_happy: int

def parse(line):
    line = line.strip().split()
    src = line[0]
    sign = 1 if line[2] == 'gain' else -1
    val = int(line[3])
    dst = line[-1][:-1]
    return Node(src, dst, sign*val)

def order(people: defaultdict[defaultdict[int]], first: str, last: str, taken: set, happiness: int=0):
    if len(taken) == len(people):
        return happiness + people[first][last] + people[last][first]
    best = 0
    for p in people:
        if p not in taken:
            best = max(best, order(people, first, p, taken | {p}, happiness + people[p][last] + people[last][p]))
    return best

def main(in_file: TextIOWrapper):
    nodes = list(map(parse, in_file.readlines()))
    deltas = defaultdict(lambda:defaultdict(int))
    for n in nodes:
        deltas[n.src][n.neighbor] = n.del_happy
    best = order(deltas, nodes[0].src, nodes[0].src, {nodes[0].src})
    print(best)
    deltas['me']
    best = order(deltas, nodes[0].src, nodes[0].src, {nodes[0].src})
    print(best)
