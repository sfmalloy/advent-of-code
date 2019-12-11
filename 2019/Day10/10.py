from collections import defaultdict

space = [line.strip() for line in open("10.test", 'r').readlines()]

asteroids = set()
for x in range(len(space)):
    for y in range(len(space[x])):
        if (space[x][y] == '#'):
            asteroids.add((x, y))

best = 0
for a in asteroids:
    seen = asteroids.copy()
    for b in asteroids:
        dy = b[1] - a[1]
        dx = b[0] - a[0]
        if (dx != 0):
            slope = dy / dx
            for c in seen:
                if (c != b and c != a and c[0] != a[0] and slope == (c[1] - a[1] / c[0] - a[0])):
                    seen.remove(c)
    best = max(best, len(seen))

print(best)

