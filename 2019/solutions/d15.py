from io import TextIOWrapper
from intcode import Intcode
from types import SimpleNamespace
from collections import namedtuple
from copy import deepcopy

const = SimpleNamespace()
const.N = 1
const.S = 2
const.W = 3
const.E = 4

def move(comp: Intcode, m):
    comp.read_in(m)
    comp.run()
    return comp.read_out()[0]

def opposite(m):
    match m:
        case const.N:
            return const.S
        case const.S:
            return const.N
        case const.W:
            return const.E
        case const.E:
            return const.W

def main(in_file: TextIOWrapper):
    comp = Intcode(in_file.readline())
    node = namedtuple('node', 'x y status path robot')
    point = namedtuple('point', 'x y')

    dx = [0,0,1,-1]
    dy = [1,-1,0,0]

    known = {}
    frontier = [node(0, 0, 1, [], comp)]
    curr = frontier.pop(0)
    
    while curr.status != 2:
        pt = point(curr.x, curr.y)
        if pt not in known:
            known[pt] = curr.status
        
        for i in range(const.N, const.E+1):
            p = point(curr.x+dx[i-1], curr.y+dy[i-1])
            bot = deepcopy(curr.robot)
            m = move(bot, i)
            if p not in known and m != 0:
                frontier.append(node(p.x, p.y, m, curr.path+[i], bot))
            elif m == 0:
                known[point(p.x, p.y)] = m
        curr = frontier.pop()
    print(len(curr.path))

    edges = [[point(curr.x, curr.y)]]
    t = 0
    while 1 in set(p[1] for p in known.items()):
        front = edges.pop(0)
        adj = []
        for f in front:
            x = f.x
            y = f.y
            for d in range(const.N, const.E+1):
                p = point(x+dx[d-1], y+dy[d-1])
                if p in known and known[p] == 1:
                    known[p] = 2
                    adj.append(p)
        edges.append(adj)
        t += 1
    print(t)
