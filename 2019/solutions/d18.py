from io import TextIOWrapper
from collections import defaultdict, deque
import heapq

HASHES = []

class Point:
    r: int
    c: int

    def __init__(self, r, c) -> None:
        self.r = r
        self.c = c

    def __add__(self, other):
        return Point(self.r + other.r, self.c + other.c)

    def __hash__(self):
        return HASHES[self.r][self.c]
    
    def __eq__(self, other):
        return self.r == other.r and self.c == other.c


DIRS = [Point(-1, 0), Point(1, 0), Point(0, -1), Point(0, 1)]

class Node:
    pos: Point
    keys: int
    dist: int

    def __init__(self, pos, keys, dist):
        self.pos = pos
        self.keys = keys
        self.dist = dist

    def __lt__(self, other):
        return self.dist < other.dist

    def __eq__(self, other):
        return self.pos == other.pos \
            and self.keys == other.keys \
            and self.dist == other.dist
    
    def __hash__(self):
        return hash((self.pos, self.keys, self.dist))


def encode_letter(letter: str):
    a = 'a' if letter.islower() else 'A'
    return 2**(ord(letter) - ord(a) + 1)


def dist_to_keys(start: Point, goals: int, keys: int, maze: list[list[int]]):
    local_q = deque([(start, 0)])
    visited = set()

    local_dists = []
    while len(local_q) > 0:
        pos, dist = local_q.popleft()
        if maze[pos.r][pos.c] > 0 and maze[pos.r][pos.c] & goals:
            local_dists.append((pos, dist))
        visited.add(pos)

        for d in DIRS:
            new = pos+d
            if (maze[new.r][new.c] > 0 or -maze[new.r][new.c] & keys) and new not in visited:
                local_q.append((new, dist+1))

    return local_dists


def pre_hash(R, C):
    hashes = []
    for r in range(R):
        row = []
        for c in range(C):
            row.append(hash((r, c)))
        hashes.append(row)
    return hashes


def solve(in_file: TextIOWrapper):
    ipt = [l.strip() for l in in_file.readlines()]
    global HASHES
    HASHES = pre_hash(len(ipt), len(ipt[0]))

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
            keys_to_find = 0
            for k, p in key_pos.items():
                if not k & node.keys:
                    keys_to_find |= k
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
    # cProfile.runctx('solve(in_file)', globals(), locals(), sort=1)
    solve(in_file)
