from intcode import Intcode
comp = list(map(int, open("11.in", 'r').read().strip().split(',')))

part1 = Intcode(comp)

def get_visited(prog, init):
    coord = [0,0]
    compass = 0
    h = [0,1,0,-1]
    v = [1,0,-1,0]
    visited = {}
    output = prog.run([init], True, 2)

    while (output != []):
        visited[tuple(coord)] = output[0]
        compass = (compass + (-1 if output[1] == 0 else 1)) % 4
        coord = [coord[0] + h[compass], coord[1] + v[compass]]
        
        next_input = 0
        if (tuple(coord) in visited):
            next_input = visited[tuple(coord)]
        output = prog.run([next_input], True, 2)
    return visited

print(len(get_visited(part1, 0)))

part2 = Intcode(comp)
visited = get_visited(part2, 1)

min_x = min_y = 1000000000000
max_x = max_y = -1000000000000

for p in visited:
    min_x = min(min_x, p[0])
    min_y = min(min_y, p[1])
    max_x = max(max_x, p[0])
    max_y = max(max_y, p[1])

print_chr = {0 : ' ', 1 : chr(9608)}
for y in range(max_y, min_y - 1, -1):
    for x in range(min_x, max_x + 1):
        if ((x,y) in visited and visited[(x,y)] == 1):
            print(print_chr[1], end='')
        else:
            print(print_chr[0], end='')
    print('')
