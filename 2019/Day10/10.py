from collections import defaultdict
from functools import total_ordering
from math import sqrt

space = [line.strip() for line in open("10.in", 'r').readlines()]

class slope_attr:
    def __init__(self, slope):
        self.slope = slope
        self.left = self.right = False

    def __hash__(self):
        return hash((self.slope, self.left, self.right))
    
    def __eq__(self, other):
        return (self.slope, self.left, self.right) == (other.slope, other.left, other.right)

    def __lt__(self, other):
        return self.slope < other.slope

    def __str__(self):
        return str((self.slope, self.left, self.right))

asteroids = set()
for y in range(len(space)):
    for x in range(len(space[y])):
        if (space[y][x] != '.'):
            asteroids.add((x, y))

best = 0
coord = (0, 0)
slopes = defaultdict(list)
for a in asteroids:
    curr = defaultdict(list)
    for b in asteroids:
        dy = b[1] - a[1]
        dx = b[0] - a[0]
        if (dx != 0):
            s = slope_attr(dy / dx)
            if (dx > 0):
                s.right = True
            else:
                s.left = True
            curr[s].append(b)
        elif (dy < 0):
            curr[slope_attr(-float("inf"))].append(b)
        elif (dy > 0):
            curr[slope_attr(float("inf"))].append(b)
    if (len(curr) > best):
        best = len(curr)
        coord = a
        slopes = curr

print("Part 1: %d" % best)

def distance(a, b):
    return sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)

t = list(slopes.keys())
t.sort()
found_asteroid = True
bopped = []

def get_closest(coord):
    closest = coord
    dist = float("inf")
    for a in slopes[s]:
        curr_dist = distance(coord, a)
        if (curr_dist < dist):
            closest = a
            dist = curr_dist
    return closest

while (found_asteroid):
    found_asteroid = False

    for s in t:
        if ((s.slope == float("inf") or s.right) and len(slopes[s]) > 0):
            closest = get_closest(coord)
            found_asteroid = closest != coord
            bopped.append(closest)
            slopes[s].remove(closest)
    for s in t:
        if ((s.slope == -float("inf") or s.left) and len(slopes[s]) > 0):
            closest = get_closest(coord)
            found_asteroid = closest != coord or found_asteroid
            bopped.append(closest)
            slopes[s].remove(closest)

winner = bopped[199]
print("Part 2: %d" % (winner[0] * 100 + winner[1]))
