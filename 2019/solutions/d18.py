from io import TextIOWrapper
from collections import deque, defaultdict
from dataclasses import dataclass
import heapq

# dataclass hash was slow, shaved some time manually defining it
class Point:
    r: int
    c: int

    def __init__(self, r, c):
        self.r = r
        self.c = c

    def __add__(self, other):
        return Point(self.r + other.r, self.c + other.c)
    
    def __eq__(self, other):
        return self.r == other.r and self.c == other.c

    def __hash__(self):
        return hash((self.r, self.c))


@dataclass
class Node:
    dist: int
    val: int
    doors: int


@dataclass
class QueueNode:
    pos: int
    dist: int
    keys: int

    def __lt__(self, other):
        return self.dist < other.dist


def encode_letter(letter: str):
    a = 'a' if letter.islower() else 'A'
    return 2**(ord(letter) - ord(a) + 1)


DIRS = [Point(-1, 0), Point(1, 0), Point(0, -1), Point(0, 1)]
def dist_to_nodes(start: Point, maze: list[list[int]]):
    q = deque([(start, 0, 0)])
    visited = set()

    dists = {}
    while len(q) > 0:
        pos, dist, doors = q.popleft()
        val = maze[pos.r][pos.c]
        if val > 1 and dist > 0:
            dists[val] = Node(dist, val, doors)
        visited.add(pos)

        for d in DIRS:
            new = pos+d
            if new not in visited:
                elem = maze[new.r][new.c]
                if elem > 0:
                    q.append((new, dist+1, doors))
                elif elem < 0:
                    q.append((new, dist+1, doors | -elem))
                    

    return dists


def main(in_file: TextIOWrapper):
    ipt = [l.strip() for l in in_file.readlines()]

    # encode the map using base-2 numbers
    maze = []
    positions = {}
    start = Point(0, 0)
    num_keys = 0
    for i,r in enumerate(ipt):
        row = []
        for j,c in enumerate(r):
            if c == '.': # empty
                row.append(1)
            elif c == '#': # wall
                row.append(0)
            elif c == '@': # robot
                row.append(1)
                start = Point(i, j)
            elif c.islower(): # key
                e = encode_letter(c)
                row.append(e)
                positions[e] = Point(i, j)
                num_keys += 1
            elif c.isupper(): # door
                row.append(-encode_letter(c))
        maze.append(row)

    all_keys = 0
    key = 2
    for i in range(num_keys):
        all_keys |= key
        key *= 2

    INF = 2**31
    graph = {}
    # precalculate BFS
    graph[1] = dist_to_nodes(start, maze)
    for val_outer, pos_outer in positions.items():
        graph[val_outer] = dist_to_nodes(pos_outer, maze)

    dists = defaultdict(lambda: defaultdict(lambda: INF))

    visited = set()
    q = [QueueNode(1, 0, 0)]
    while len(q) > 0:
        node = heapq.heappop(q)
        if node.keys == all_keys:
            print(node.dist)
            break
        if (node.pos, node.keys) in visited:
            continue
        visited.add((node.pos, node.keys))
        for key in positions.keys():
            if not key & node.keys:
                elem = graph[node.pos][key]
                dist = node.dist + graph[node.pos][key].dist
                if (elem.doors | node.keys) == node.keys and dist < dists[key][node.keys | key]:
                    heapq.heappush(q, QueueNode(key, node.dist + graph[node.pos][key].dist, node.keys | key))
