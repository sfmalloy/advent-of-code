from io import TextIOWrapper
from dataclasses import dataclass
from collections import defaultdict

class Dir:
    N = 0
    E = 1
    S = 2
    W = 3

    dr = [-1,0,1,0]
    dc = [0,1,0,-1]

@dataclass(frozen=True, eq=True)
class State:
    r: int
    c: int
    keys: list[str]

g_cache = {}
g_paths = defaultdict(list)

def get_paths(r, c, goal, maze, visited=set()):
    if (r, c, goal) in g_cache:
        return g_cache[(r, c, goal)]
    if maze[r][c] == goal:
        return goal
    min_path = ''
    for d in range(Dir.N, Dir.W+1):
        new_r = r + Dir.dr[d]
        new_c = c + Dir.dc[d]
        if maze[new_r][new_c] != '#' and (new_r, new_c) not in visited:
            curr = maze[r][c] + get_paths(new_r, new_c, goal, maze, visited | {(r,c)})
            if curr != maze[r][c] and (len(curr) < len(min_path) or min_path == ''):
                min_path = curr
    if min_path != '':
        g_cache[(r, c, goal)] = min_path
    return min_path

def get_key_paths(curr_key, key_points, maze):
    dists = {}
    r, c = key_points[curr_key]
    for k in key_points.keys():
        if k != curr_key:
            dists[k] = get_paths(r, c, k, maze)
    return dists

def memoize(f):
    memo = {}
    def helper(curr, raw, filtered, key_limit, keys=set(), seen=set()):
        tkeys = tuple(sorted(keys))
        tseen = tuple(sorted(seen))
        if (curr, tkeys, tseen) not in memo:
            memo[(curr, tkeys, tseen)] = f(curr, raw, filtered, key_limit, keys, seen)
        return memo[(curr, tkeys, tseen)]
    return helper

@memoize
def get_min_path(curr, raw, filtered, key_limit, keys=set(), seen=set()):
    if len(keys) == key_limit:
        return 0
    starts = []
    for p in filtered[curr].values():
        i = 0
        while i < len(p) and (p[i] in seen or p[i].lower() in keys):
            i += 1
        if i < len(p) and p[i].islower():
            starts.append(p[i])
    
    dist = 1000000000000
    for s in starts:
        if s not in seen:
            dist = min(dist, len(raw[curr][s]) - 1 + get_min_path(s, raw, filtered, key_limit, keys | {s}, seen | {curr}))
    return dist

def part_one(maze):
    keys = 0
    goals = {}
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c].islower():
                keys += 1
            if maze[r][c] not in '.#':
                goals[maze[r][c]] = (r,c)

    raw_paths = {}
    filtered_paths = defaultdict(dict)
    for k in goals:
        raw_paths[k] = get_key_paths(k, goals, maze)
        for p in raw_paths[k]:
            path = ''
            for c in raw_paths[k][p]:
                if c not in f'.@':
                    path += c
            filtered_paths[k][p] = path
    
    for k in goals:
        to_remove = []
        for g1,p1 in filtered_paths[k].items():
            for g2,p2 in filtered_paths[k].items():
                if g1 != g2 and p1 in p2:
                    to_remove.append(g1)
                    break
        for t in to_remove:
            filtered_paths[k].pop(t)

    print(get_min_path('@', raw_paths, filtered_paths, keys))

def main(in_file: TextIOWrapper):
    maze = [list(map(str, l.strip())) for l in in_file.readlines()]
    part_one(maze)
