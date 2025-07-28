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

    def __str__(self):
        return f'Point({self.r}, {self.c})'

    def __repr__(self) -> str:
        return self.__str__()


@dataclass
class Node:
    dist: int
    val: int
    doors: int


@dataclass
class QueueNode:
    pos: list[int]
    dist: int
    keys: int

    def __lt__(self, other):
        return self.dist < other.dist
    

def encode_letter(letter: str):
    a = 'a' if letter.islower() else 'A'
    return 2**(ord(letter) - ord(a) + 4)


DIRS = [Point(-1, 0), Point(1, 0), Point(0, -1), Point(0, 1)]
def dist_to_nodes(start: Point, maze: list[list[int]]):
    q = deque([(start, 0, 0)])
    visited = set()

    dists = {}
    while len(q) > 0:
        pos, dist, doors = q.popleft()
        val = maze[pos.r][pos.c]
        if val >= 16 and dist > 0:
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


def get_min_dist(ipt: list[str]):
    # encode the map using base-2 numbers
    maze = []
    positions = {}
    starts = []
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
                starts.append(Point(i, j))
            elif c.islower(): # key
                e = encode_letter(c)
                row.append(e)
                positions[e] = Point(i, j)
                num_keys += 1
            elif c.isupper(): # door
                row.append(-encode_letter(c))
        maze.append(row)

    all_keys = 0
    key = 16
    for i in range(num_keys):
        all_keys |= key
        key *= 2

    INF = 2**31
    graph = {}
    # precalculate BFS
    for i,start in enumerate(starts):
        graph[2**i] = dist_to_nodes(start, maze)
    for val_outer, pos_outer in positions.items():
        graph[val_outer] = dist_to_nodes(pos_outer, maze)

    dists = defaultdict(lambda: defaultdict(lambda: INF))

    visited = set()
    q = [QueueNode([2**i for i in range(len(starts))], 0, 0)]
    while len(q) > 0:
        node = heapq.heappop(q)
        if node.keys == all_keys:
            return node.dist
        
        t = tuple(node.pos) + (node.keys,)
        if t in visited:
            continue
        visited.add(t)
        for i,pos in enumerate(node.pos):
            for key in positions.keys():
                if not key & node.keys and key in graph[pos]:
                    elem = graph[pos][key]
                    dist = node.dist + graph[pos][key].dist
                    if (elem.doors | node.keys) == node.keys and dist < dists[key][node.keys | key]:
                        new_pos = [p for p in node.pos]
                        new_pos[i] = key
                        heapq.heappush(q, QueueNode(new_pos, node.dist + graph[pos][key].dist, node.keys | key))


def get_part1_start(ipt: list[str]):
    for i,r in enumerate(ipt):
        for j,c in enumerate(r):
            if c == '@':
                return Point(i, j)


def main(in_file: TextIOWrapper):
    ipt = [[c for c in l.strip()] for l in in_file.readlines()]
    start = get_part1_start(ipt)

    part1 = get_min_dist(ipt)

    ipt[start.r-1][start.c-1:start.c+2] = '@#@'
    ipt[start.r][start.c-1:start.c+2] = '###'
    ipt[start.r+1][start.c-1:start.c+2] = '@#@'
    part2 = get_min_dist(ipt)

    print(part1)
    print(part2)
