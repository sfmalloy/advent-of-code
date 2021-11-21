# use dijkstra's
from collections import namedtuple
from copy import deepcopy
from io import TextIOWrapper

edge = namedtuple('edge', 'name length')
class node:
    def __init__(self, name):
        self.name = name
        self.dist = float('inf')
        self.connects = []
    def add(self, dst, dist):
        self.connects.append(edge(dst, dist))
    def __str__(self):
        return f'{(self.name, self.dist)}, {self.connects}'
    def __repr__(self):
        return self.__str__()

def short_path(nodes, start):
    nodes[start].dist = 0
    curr = start
    pathlen = 0
    while len(nodes) > 0:
        next_node = edge('', float('inf'))
        for n in nodes[curr].connects:
            if n.name in nodes:
                nodes[n.name].dist = nodes[curr].dist + n.length
                if nodes[n.name].dist < next_node.length:
                    next_node = edge(n.name, nodes[n.name].dist)
        nodes.pop(curr)
        if next_node.length != float('inf'):
            pathlen = next_node.length
        curr = next_node.name
    return pathlen


def long_path(nodes, start):
    for n in nodes:
        nodes[n].dist = -float('inf')
    nodes[start].dist = 0
    curr = start
    pathlen = 0
    while len(nodes) > 0:
        next_node = edge('', -float('inf'))
        for n in nodes[curr].connects:
            if n.name in nodes:
                nodes[n.name].dist = nodes[curr].dist + n.length
                if nodes[n.name].dist > next_node.length:
                    next_node = edge(n.name, nodes[n.name].dist)
        nodes.pop(curr)
        if next_node.length != -float('inf'):
            pathlen = next_node.length
        curr = next_node.name
    return pathlen

def main(in_file: TextIOWrapper):
    nodes = {}
    for l in in_file.readlines():
        l = l.rstrip().split()
        src = l[0]
        dst = l[2]
        dist = int(l[-1])
        if src not in nodes:
            nodes[src] = node(src)
        nodes[src].add(dst, dist)
        if dst not in nodes:
            nodes[dst] = node(src)
        nodes[dst].add(src, dist)

    shortest = float('inf')
    for n in nodes:
        shortest = min(short_path(deepcopy(nodes), n), shortest)
    print(shortest)

    longest = -float('inf')
    for n in nodes:
        longest = max(long_path(deepcopy(nodes), n), longest)
    print(longest)