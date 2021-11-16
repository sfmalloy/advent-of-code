from io import TextIOWrapper
from collections import defaultdict

def get_slope(src_x, src_y, dst_x, dst_y):
    if dst_x == src_x:
        return (dst_y - src_y) * float('inf')
    return (dst_y - src_y) / (dst_x - src_x)

def get_distance(src_x, src_y, dst_x, dst_y):
    return ((src_y - dst_y)**2 + (src_x - dst_x)**2) ** 0.5

def find_closest(src, points):
    min_dist = float('inf')
    min_point = None
    for p_x, p_y in points:
        dist = get_distance(src[0], src[1], p_x, p_y)
        if dist < min_dist:
            min_dist = dist
            min_point = (p_x, p_y)
    return min_point

def main(in_file: TextIOWrapper):
    grid = []
    for line in in_file.readlines():
        grid.append(list(map(str, line.strip())))

    final_slopes = defaultdict(list)
    max_point = (0, 0)
    max_count = 0
    for src_y in range(len(grid)):
        for src_x in range(len(grid[src_y])):
            if grid[src_y][src_x] == '#':
                slopes = defaultdict(list)
                curr_count = 0
                
                for dst_y in range(len(grid)):
                    for dst_x in range(len(grid[dst_y])):
                        if grid[dst_y][dst_x] == '#' and not (src_x == dst_x and src_y == dst_y):
                            curr_slope = get_slope(src_x, src_y, dst_x, dst_y)
                            slopes[curr_slope].append((dst_x, dst_y))
                            if len(slopes[curr_slope]) == 1:
                                curr_count += 1
                
                for s in slopes.values():
                    first_x, first_y = s[0]
                    last_x, last_y = s[-1]
                    if (first_y < src_y and last_y > src_y) or (first_x < src_x and last_x > src_x):
                        curr_count += 1

                if curr_count > max_count:
                    max_count = curr_count
                    max_point = (src_x, src_y)
                    final_slopes = slopes

    print(max_count)

    keys = list(sorted(final_slopes.keys()))

    right = defaultdict(list)
    left = defaultdict(list)

    for k in keys:
        for p in final_slopes[k]:
            if p[0] < max_point[0]:
                left[k].append(p)
            else:
                right[k].append(p)
    
    num_bopped = 0
    stop = 200
    while num_bopped < stop:
        for slope in right:
            if len(right[slope]) > 0:
                closest = find_closest(max_point, right[slope])
                right[slope].remove(closest)
                num_bopped += 1
                if num_bopped == stop:
                    print(closest[0]*100 + closest[1])
                    break

        if num_bopped < stop:
            for slope in left:
                if (len(left[slope])) > 0:
                    closest = find_closest(max_point, left[slope])
                    left[slope].remove(closest)
                    num_bopped += 1
                    if num_bopped == stop:
                        print(closest[0]*100 + closest[1])
                        break


