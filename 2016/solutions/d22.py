import re
from io import TextIOWrapper
from dataclasses import dataclass
from collections import deque


@dataclass(eq=True)
class Node:
    x: int
    y: int
    size: int
    used: int

    def avail(self):
        return self.size - self.used


def main(file: TextIOWrapper):
    lines = [line.strip() for line in file.readlines()]
    nodes = dict()
    for line in lines[2:]:
        node = Node(*map(int, re.findall(r'\d+', line)[:-2]))
        nodes[node.x, node.y] = node
    return part1(nodes), part2(nodes)


def part1(nodes: dict[tuple[int, int], Node]):
    pairs = set()
    for a in nodes.values():
        if not a.used:
            continue
        for b in nodes.values():
            if a == b:
                continue
            if a.used <= b.avail():
                pairs.add((a.x, a.y, b.x, b.y))
    return len(pairs)


def part2(nodes: dict[tuple[int, int], Node]):
    right = 0
    empty = None
    for node in nodes.values():
        right = max(right, node.x)
        if node.used == 0:
            empty = (node.x, node.y)
    path = []
    while right > 0:
        path += move_goal(right, 0, empty[0], empty[1], nodes)
        path.pop()
        empty = (right, 0)
        right -= 1
    return len(path)


def move_goal(gx: int, gy: int, ex: int, ey: int, nodes: dict[tuple[int, int], Node]):
    q = deque([(ex, ey, ex, ey, [])])
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    visited = set()
    visited.add((gx, gy))
    assert nodes[ex, ey].used == 0
    goal_path = []
    while q:
        x, y, prev_x, prev_y, path = q.popleft()
        if x == gx-1 and y == gy:
            goal_path = path + [(gx-1, gy)]
            break
        if (x, y, prev_x, prev_y) in visited:
            continue
        visited.add((x, y, prev_x, prev_y))
        for dx, dy in dirs:
            new = (x+dx, y+dy)
            if (
                new in nodes 
                and new not in visited 
                and nodes[x, y].size >= nodes[new].used
            ):
                q.append((new[0], new[1], x, y, path + [(x, y)]))

    goal_path.append((gx, gy))
    for i in range(len(goal_path)-1):
        nodes[goal_path[i]].used, nodes[goal_path[i+1]].used = nodes[goal_path[i+1]].used, nodes[goal_path[i]].used
    return goal_path
