from io import TextIOWrapper
from dataclasses import dataclass
from collections import defaultdict, deque
from queue import PriorityQueue
import heapq


@dataclass(frozen=True, eq=True)
class Point:
    r: int
    c: int

    def __add__(self, other):
        return Point(self.r + other.r, self.c + other.c)


@dataclass(frozen=True, eq=True)
class Node:
    pos: Point
    keys: int
    dist: int

    def __lt__(self, other):
        return self.dist < other.dist


def encode_letter(letter: str):
    a = 'a' if letter.islower() else 'A'
    return 2**(ord(letter) - ord(a) + 1)


DIRS = [Point(-1, 0), Point(1, 0), Point(0, -1), Point(0, 1)]

def dist_to_keys(start: Point, goals: set[Point], keys: int, maze: list[list[int]]):
    local_q = deque([(start, 0)])
    visited = set()

    local_dists = []
    while len(local_q) > 0 and len(local_dists) < len(goals):
        pos, dist = local_q.popleft()
        if pos in goals:
            local_dists.append((pos, dist))
        visited.add(pos)

        for d in DIRS:
            new = pos+d
            if (maze[new.r][new.c] > 0 or -maze[new.r][new.c] & keys) and new not in visited:
                local_q.append((new, dist+1))

    return local_dists


def solve(in_file: TextIOWrapper):
    ipt = [l.strip() for l in in_file.readlines()]
    maze = []
    start = Point(0, 0)
    num_keys = 0
    key_pos = {}
    pos_key = {}
    for i,r in enumerate(ipt):
        row = []
        for j,c in enumerate(r):
            if c == '.':
                row.append(1)
            elif c == '#':
                row.append(0)
            elif c == '@':
                row.append(1)
                start = Point(i, j)
            elif c.islower():
                e = encode_letter(c)
                row.append(e)
                key_pos[e] = Point(i, j)
                pos_key[Point(i, j)] = e
                num_keys += 1
            elif c.isupper():
                row.append(-encode_letter(c))
        maze.append(row)

    all_keys = 0
    key = 2
    for i in range(num_keys):
        all_keys |= key
        key *= 2

    INF = 2**31
    dists = defaultdict(lambda: defaultdict(lambda: INF))
    dist_to_key_cache = {}

    q = []
    starting_node = Node(start, 0, 0)
    heapq.heappush(q, starting_node)
    while len(q) > 0:
        node: Node = heapq.heappop(q)
        if node.keys == all_keys:
            print(node.dist)
            break
        
        local_dists = []
        if (node.pos, node.keys) in dist_to_key_cache:
            local_dists = dist_to_key_cache[(node.pos, node.keys)]
        else:
            keys_to_find = set()
            for k, p in key_pos.items():
                if not k & node.keys:
                    keys_to_find.add(p)
            local_dists = dist_to_keys(node.pos, keys_to_find, node.keys, maze)
            dist_to_key_cache[(node.pos, node.keys)] = local_dists

        for (p, d) in local_dists:
            k = pos_key[p]
            if d and node.dist + d < dists[node.keys][k]:
                dists[node.keys][k] = node.dist + d
                new_node = Node(p, node.keys|k, dists[node.keys][k])
                heapq.heappush(q, new_node)


import cProfile
def main(in_file: TextIOWrapper):
    cProfile.runctx('solve(in_file)', globals(), locals(), sort=1)
    # solve(in_file)
