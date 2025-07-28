from intcode import Intcode
from time import sleep

with open('13.in', 'r') as readfile:
  prog = list(map(int, readfile.readline().split(',')))
  comp = Intcode(prog)

# Panel types
EMPTY  = 0
WALL   = 1
BLOCK  = 2
PADDLE = 3
BALL   = 4

TILE_SYMBOLS = [' ', '#', '█', '_', 'o']
WIDTH = 0
HEIGHT = 0

def prtscn(screen):
  for y in range(HEIGHT+1):
    for x in range(WIDTH+1):
      print(TILE_SYMBOLS[screen[(x, y)]], end='')
    print()

game = comp.run()
block_count = 0
screen = {}



ball_pos = (0, 0)
paddle_pos = (0, 0)

for i in range(0, len(game) - 2, 3):
  x = game[i]
  y = game[i + 1]
  tile = game[i + 2]

  WIDTH = max(x, WIDTH)
  HEIGHT = max(y, HEIGHT)

  screen[(x, y)] = tile

  if tile == BLOCK:
    block_count += 1
  elif tile == BALL:
    ball_pos = (x, y)
  elif tile == PADDLE:
    paddle_pos = (x, y)

print(block_count)

prog[0] = 2
comp = Intcode(prog)
output = comp.run(early_return=True, early_count=3)
while output is not None:
  output = comp.run(early_return=True, early_count=3)

score = 0
def update(move):
  output = comp.run(readin=[move], early_return=True, early_count=3)
  if output is None:
    return True
  while output is not None:
    x, y, tile = output
    screen[(x, y)] = tile

    if tile == BALL:
      global ball_pos
      ball_pos = (x, y)
    elif tile == PADDLE:
      global paddle_pos
      paddle_pos = (x, y)
    elif x == -1:
      global score
      score = output[2]

    output = comp.run(early_return=True, early_count=3)

  return False
# 'ai' time lol
move = 0
while not update(move):
  # prtscn(screen)
  if ball_pos[0] == paddle_pos[0] + 1:
    move = 1
  elif ball_pos[0] == paddle_pos[0] - 1:
    move = -1
  else:
    move = 0

print(score)