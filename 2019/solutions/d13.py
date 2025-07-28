from io import TextIOWrapper
from intcode import Intcode
from time import sleep

class Move:
    LEFT  = -1
    RIGHT = 1
    STAY  = 0

class Tiles:
    EMPTY  = 0
    WALL   = 1
    BLOCK  = 2
    PADDLE = 3
    BALL   = 4

def print_screen(screen):
    TILES = ' |#_*'
    
    for y in range(len(screen)):
        for x in range(len(screen[0])):
            print(TILES[screen[y][x]], end='')
        print()

def main(in_file: TextIOWrapper):
    game = Intcode(in_file.readline())
    game.run()
    init_state = game.read_out()
    Y, X = init_state[-3] + 1, init_state[-2] + 1
    
    screen = [[0 for _ in range(Y)] for _ in range(X)]

    block_count = 0
    i = 0
    while i < len(init_state):
        x, y, tile = init_state[i:i+3]
        screen[y][x] = tile
        block_count += tile == Tiles.BLOCK
        i += 3
    print(block_count)
    
    ###########################################################
    # Part 2
    game.reset()
    game.program[0] = 2
    game.run()
    init_state = game.read_out()

    i = 0
    while i < len(init_state):
        x, y, tile = init_state[i:i+3]
        screen[y][x] = tile
        i += 3

    paddle_x = ball_x = -1
    while game.run() != 99:
        output = game.read_out()
        i = 0
        while i < len(output):
            x, y, tile = output[i:i+3]
            if x != -1:
                screen[y][x] = tile
                match tile:
                    case Tiles.PADDLE:
                        ball_x = x
                    case Tiles.BALL:
                        paddle_x = x
            i += 3

        if paddle_x < ball_x:
            next_move = Move.LEFT
        elif paddle_x > ball_x:
            next_move = Move.RIGHT
        else:
            next_move = Move.STAY
        game.read_in(next_move)
    print(game.read_out()[-1])
