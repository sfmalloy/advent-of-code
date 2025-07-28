from io import TextIOWrapper
from collections import defaultdict
from copy import deepcopy

def count_orbits(start, orbits):
    c = 0
    if start in orbits:
        for o in orbits.get(start):
            c += 1 + count_orbits(o, orbits)
    return c

def find_path_helper(start, end, orbits, seen, length):
    if start == end:
        return length - 2
    if start in orbits:
        for o in orbits.get(start):
            if o not in seen:
                seen.add(o)
                l = find_path_helper(o, end, orbits, seen, length + 1)
                if l > 0:
                    return l
    return 0

def find_path(start, end, orbits):
    extended_orbits = deepcopy(orbits)
    for outer, inner in orbits.items():
        for planet in inner:
            extended_orbits[planet].append(outer)

    return find_path_helper(start, end, extended_orbits, {start}, 0)

def main(in_file: TextIOWrapper):
    lines = list(map(lambda s: s.strip().split(')'), in_file.readlines()))
    orbits = defaultdict(list)

    for l in lines:
        orbits[l[0]].append(l[1])
    total = 0
    for o in orbits:
        total += count_orbits(o, orbits)
    print(total)
    print(find_path('YOU', 'SAN', orbits))
