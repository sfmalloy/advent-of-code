from collections import defaultdict

def combine_moves(curr_path, moves):
    paths = []

    for m in moves:
        p = curr_path.copy()
        p.append(m)
        paths.append(p)
    return paths

def valid_path(path, key):
    return path[-1] == key

connections = [line.strip() for line in open("6.in",'r').readlines()]
move_map = defaultdict(list)
nodes = set()

for node in connections:
    a,b = node.split(')')
    move_map[a].append(b)
    nodes.add(a)
    nodes.add(b)
    
orbits = 0
keys = move_map.keys()
you_path = []
san_path = []
for n in nodes:
    frontier = [['COM']]
    curr_path = frontier[0]
    while (not valid_path(curr_path, n)):
        end = curr_path[-1]
        if (end in keys):
            moves = move_map[curr_path[-1]]
            frontier += combine_moves(curr_path, moves)
        curr_path = frontier.pop(0)
    
    if (n == 'YOU'):
        you_path = curr_path
    if (n == 'SAN'):
        san_path = curr_path
    orbits += len(curr_path) - 1

print("Part 1: %d" % orbits)

split = ''
i = j = 0
while (you_path[i] in san_path[i]):
    i += 1
while (san_path[j] in you_path[j]):
    j += 1

print("Part 2: %d" % (len(you_path) + len(san_path) - (i + j) - 2))
