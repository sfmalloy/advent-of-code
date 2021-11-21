from io import TextIOWrapper

def main(in_file: TextIOWrapper):
    cmds = in_file.readlines()

    grid = [[False for _ in range(1000)] for _ in range(1000)]
    bright = [[0 for _ in range(1000)] for _ in range(1000)]

    for cmd in cmds:
        cmd = cmd.split()
        if cmd[0] == 'turn':
            state = cmd[1] == 'on'
            brightness = 1 if state else -1
            ra, ca = map(int, cmd[2].split(','))
            rb, cb = map(int, cmd[4].split(','))

            for r in range(ra, rb+1):
                for c in range(ca, cb+1):
                    grid[r][c] = state
                    bright[r][c] += brightness
                    if bright[r][c] < 0:
                        bright[r][c] = 0
        else:
            ra, ca = map(int, cmd[1].split(','))
            rb, cb = map(int, cmd[3].split(','))
        
            for r in range(ra, rb+1):
                for c in range(ca, cb+1):
                    grid[r][c] = not grid[r][c]
                    bright[r][c] += 2

    on = 0
    for r in grid:
        for c in r:
            on += int(c)

    print(on)
    print(sum(sum(b) for b in bright))
