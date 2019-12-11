space = [line.strip() for line in open("10.test", 'r').readlines()]

class slope_attr:
    def __init__(self, slope):
        self.slope = slope
        self.left = self.right = False

    def __hash__(self):
        return hash((self.slope, self.left, self.right))
    
    def __eq__(self, other):
        return (self.slope, self.left, self.right) == (other.slope, other.left, other.right)

    def __str__(self):
        return str((self.slope, self.left, self.right))

asteroids = set()
for y in range(len(space)):
    for x in range(len(space[y])):
        if (space[y][x] != '.'):
            asteroids.add((x, y))

best = 0
coord = (0, 0)
discovered = []
for a in asteroids:
    slopes = set()
    found = []
    for b in asteroids:
        dy = a[1] - b[1]
        dx = a[0] - b[0]
        if (dx != 0):
            s = slope_attr(dy / dx)
            if (dx < 0):
                s.right = True
            else:
                s.left = True
            slopes.add(s)
            found.add(b)
        elif (dy < 0):
            s = slope_attr(float("inf"))
            slopes.add(s)
            found.add(b)
        elif (dy > 0):
            s = slope_attr(-float("inf"))
            slopes.add(s)
            found.add(b)
    if (len(slopes) > best):
        best = len(slopes)
        coord = a
print(best, coord)

laser = [0,0]
boomed = []
while (len(asteroids) > 1):
    
