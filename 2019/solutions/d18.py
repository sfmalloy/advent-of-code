from io import TextIOWrapper
from dataclasses import dataclass, field
from collections import defaultdict
from multiprocessing.process import current_process
from queue import PriorityQueue, Queue
from copy import deepcopy
from pprint import pprint
from multiprocessing import Process, Value

class Dir:
    N = 0
    E = 1
    S = 2
    W = 3

    dx = [0,1,0,-1]
    dy = [-1,0,1,0]

@dataclass(eq=True)
class KeyDoorPair:
    door: tuple[int, int] = (-1, -1)
    key: tuple[int, int] = (-1, -1)

@dataclass(frozen=True, eq=True)
class State:
    x: int
    y: int
    maze: list[list[str]]
    key_door_pairs: defaultdict[KeyDoorPair]
    keys: list[str] = field(default_factory=list)
    priority: int = 0
    steps: int = 0
    seen: set[tuple[list[str]]] = field(default_factory=set)
    path: list[tuple[int, int]] = field(default_factory=list)

    def __lt__(self, other):
        return self.priority < other.priority
    
    def make_next_states(self):
        next_states = []
        for d in range(Dir.N, Dir.W+1):
            x = self.x + Dir.dx[d]
            y = self.y + Dir.dy[d]
            if self.maze[y][x] != '#' and not self.maze[y][x].isupper():
                maze = deepcopy(self.maze)
                maze[self.y][self.x] = '.'
                keys = self.keys.copy()
                if maze[y][x].islower():
                    keys.append(maze[y][x])
                    door_x, door_y = self.key_door_pairs.get(keys[-1]).door
                    if door_x != -1:
                        maze[door_x][door_y] = '.'
                maze[y][x] = '@'
                steps = self.steps + 1
                priority = steps
                seen = self.seen | {State.hashable_maze(maze)}
                path = self.path.copy() + [(x, y)]
                if len(seen) - len(self.seen) != 0:
                    next_states.append(State(x, y, maze, self.key_door_pairs, keys, priority, steps, seen, path))
        return next_states
    
    @staticmethod
    def hashable_maze(maze):
        h = ''
        for r in maze:
            for c in r:
                h += c
        return h

def main(in_file: TextIOWrapper):
    maze = [list(map(str, l.strip())) for l in in_file.readlines()]
    key_door_pairs = defaultdict(KeyDoorPair)
    x = y = 0
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c].isupper():
                key_door_pairs[maze[r][c].lower()].door = (r, c)
            elif maze[r][c].islower():
                key_door_pairs[maze[r][c]].key = (r, c)
            elif maze[r][c] == '@':
                y = r
                x = c
    
    curr = State(x, y, maze, key_door_pairs, seen={State.hashable_maze(maze)})
    q = Queue()

    while len(curr.keys) < len(key_door_pairs):
        for s in curr.make_next_states():
            q.put(s)
        curr = q.get()

    prev_x, prev_y = x, y
    for px, py in curr.path:
        maze[py][px] = '@'
        maze[prev_y][prev_x] = '.'
        prev_x, prev_y = px, py
        for r in maze:
            print(''.join(r))
        print()
    print(curr.steps)
    
