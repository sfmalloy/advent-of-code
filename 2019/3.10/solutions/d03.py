from io import TextIOWrapper

X = 0
Y = 1
g_deltas = {'R':(1,0), 'L':(-1,0), 'U':(0,1), 'D':(0,-1)}

def get_points(dirs):
    points = []
    x = y = 0
    for m in dirs:
        dir = m[0]
        dist = int(m[1:])
        while dist > 0:
            x += g_deltas[dir][X]
            y += g_deltas[dir][Y]
            dist -= 1
            point = (x,y)
            points.append(point)
    return points

def main(in_file: TextIOWrapper):
    g1, g2 = [g.split(',') for g in in_file.read().strip().splitlines()]
    p1 = get_points(g1)
    p2 = get_points(g2)

    intersections = set(p1) & set(p2)

    closest = min(intersections, key=lambda p:abs(p[X])+abs(p[Y]))
    print(abs(closest[X]) + abs(closest[Y]))

    min_sum = float('inf')
    for p in intersections:
        min_sum = min(min_sum, p1.index(p) + p2.index(p))
    print(min_sum)
