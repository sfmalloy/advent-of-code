from io import TextIOWrapper
from dataclasses import dataclass
from collections import deque
from _md5 import md5

@dataclass(frozen=True, eq=True)
class Node:
    r: int = 0
    c: int = 0
    path: str = ''

    def hash(self, passcode: str) -> str:
        return md5((passcode+self.path).encode()).hexdigest()


def main(file: TextIOWrapper):
    passcode = file.read().strip()
    goal = Node(3, 3)
    q: deque[Node] = deque()
    q.append(Node())

    p1 = Node()
    while len(q) > 0:
        curr = q.popleft()
        if curr.r == goal.r and curr.c == goal.c:
            p1 = curr
            break
        doors = curr.hash(passcode)
        
        up = Node(curr.r-1, curr.c, curr.path+'U')
        if up.r >= 0 and int(doors[0], 16) > 0xa:
            q.append(up)
        down = Node(curr.r+1, curr.c, curr.path+'D')
        if down.r < 4 and int(doors[1], 16) > 0xa:
            q.append(down)
        left = Node(curr.r, curr.c-1, curr.path+'L')
        if left.c >= 0 and int(doors[2], 16) > 0xa:
            q.append(left)
        right = Node(curr.r, curr.c+1, curr.path+'R')
        if right.c < 4 and int(doors[3], 16) > 0xa:
            q.append(right)
    
    p2 = Node()
    while len(q) > 0:
        curr = q.popleft()
        if curr.r == goal.r and curr.c == goal.c:
            p2 = curr
            continue
        doors = curr.hash(passcode)
        
        up = Node(curr.r-1, curr.c, curr.path+'U')
        if up.r >= 0 and int(doors[0], 16) > 0xa:
            q.append(up)
        down = Node(curr.r+1, curr.c, curr.path+'D')
        if down.r < 4 and int(doors[1], 16) > 0xa:
            q.append(down)
        left = Node(curr.r, curr.c-1, curr.path+'L')
        if left.c >= 0 and int(doors[2], 16) > 0xa:
            q.append(left)
        right = Node(curr.r, curr.c+1, curr.path+'R')
        if right.c < 4 and int(doors[3], 16) > 0xa:
            q.append(right)

    return p1.path, len(p2.path)
