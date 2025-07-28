from io import TextIOWrapper
from dataclasses import dataclass


def main(file: TextIOWrapper):
    R = 6
    C = 50
    screen = [[False for _ in range(C)] for _ in range(R)]
    for line in file.readlines():
        instruction = line.strip().split()
        match instruction:
            case ['rect', dims]:
                a, b = map(int, dims.split('x'))
                for r in range(b):
                    for c in range(a):
                        screen[r][c] = True
            case ['rotate', 'row', y_start, 'by', amt]:
                new_row = [False for _ in range(C)]
                r = int(y_start[2:])
                amt = int(amt)
                for c, pixel in enumerate(screen[r]):
                    new_row[(c+amt)%C] = pixel
                screen[r] = new_row
            case ['rotate', 'column', x_start, 'by', amt]:
                new_col = [False for _ in range(R)]
                c = int(x_start[2:])
                amt = int(amt)
                for r, row in enumerate(screen):
                    new_col[(r+amt)%R] = row[c]
                for r in range(R):
                    screen[r][c] = new_col[r]
    
    on = 0
    screen_str = ''
    for r in screen:
        for c in r:
            on += c
            screen_str += '█' if c else ' '
        screen_str += '\n'

    return on,screen_str
