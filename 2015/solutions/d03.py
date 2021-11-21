from io import TextIOWrapper

def main(in_file: TextIOWrapper):
    x = y = 0
    dx = {'^': 0, '<': -1, 'v': 0, '>': 1}
    dy = {'^': 1, '<': 0, 'v': -1, '>': 0}
    visited = {(0,0)}

    path = in_file.readline().strip()
    for c in path:
        x += dx[c]
        y += dy[c]
        visited.add((x,y))
    print(len(visited))

    sx = sy = rx = ry = 0
    svisited = {(0,0)}
    rvisited = {(0,0)}
    for i, c in enumerate(path):
        if i & 1:
            sx += dx[c]
            sy += dy[c]
            svisited.add((sx,sy))
        else:
            rx += dx[c]
            ry += dy[c]
            rvisited.add((rx,ry))
    print(len(svisited | rvisited))
