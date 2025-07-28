from io import TextIOWrapper
from dataclasses import dataclass
from functools import lru_cache
from collections import deque


@dataclass(frozen=True, eq=True)
class Point:
    x: int
    y: int


@lru_cache(maxsize=None)
def is_filled(x: int, y: int, fav: int):
    dec = x*x + 3*x + 2*x*y + y + y*y + fav
    ones = 0
    while dec > 0:
        ones += dec & 1
        dec >>= 1
    return ones & 1


def count(start: Point, fav: int):
    q: deque[tuple[int, Point]] = deque()
    q.append((0, start))
    seen = set()
    while len(q) > 0:
        steps, curr = q.popleft()
        seen.add(curr)
        if steps == 50:
            continue

        right = Point(curr.x+1, curr.y)
        if right not in seen and not is_filled(right.x, right.y, fav):
            q.append((steps+1, right))

        left = Point(curr.x-1, curr.y)
        if left not in seen and left.x >= 0 and not is_filled(left.x, left.y, fav):
            q.append((steps+1, left))
        
        down = Point(curr.x, curr.y+1)
        if down not in seen and not is_filled(down.x, down.y, fav):
            q.append((steps+1, down))
        
        up = Point(curr.x, curr.y-1)
        if up not in seen and up.y >= 0 and not is_filled(up.x, up.y, fav):
            q.append((steps+1, up))

    return len(seen)


def main(file: TextIOWrapper):
    fav = int(file.read().strip())
    goal = Point(31, 39)
    q: deque[tuple[int, Point]] = deque()
    q.append((0, Point(1, 1)))
    seen = set()
    min_steps = 0
    while len(q) > 0:
        steps, curr = q.popleft()
        if curr == goal:
            min_steps = steps
            break
        seen.add(curr)

        right = Point(curr.x+1, curr.y)
        if right not in seen and not is_filled(right.x, right.y, fav):
            q.append((steps+1, right))

        left = Point(curr.x-1, curr.y)
        if left not in seen and left.x >= 0 and not is_filled(left.x, left.y, fav):
            q.append((steps+1, left))
        
        down = Point(curr.x, curr.y+1)
        if down not in seen and not is_filled(down.x, down.y, fav):
            q.append((steps+1, down))
        
        up = Point(curr.x, curr.y-1)
        if up not in seen and up.y >= 0 and not is_filled(up.x, up.y, fav):
            q.append((steps+1, up))

    is_filled.cache_clear()
    return min_steps,count(Point(1, 1), fav)
