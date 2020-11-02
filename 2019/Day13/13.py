from intcode import Intcode

with open('13.in', 'r') as readfile:
  prog = list(map(int, readfile.readline().split(',')))
  comp = Intcode(prog.copy())

# Panel types
EMPTY  = 0
WALL   = 1
BLOCK  = 2
PADDLE = 3
BALL   = 4
TILE_SYMBOLS = [' ', '#', '█', '_', 'o']

game = comp.run()
block_count = 0
max_x = 0
max_y = 0

for i in range(0, len(game) - 2, 3):
  x = game[i]
  y = game[i + 1]
  tile = game[i + 2]

  max_x = max(x, max_x)
  max_y = max(y, max_y)

  if tile == BLOCK:
    block_count += 1
  

def print_game(game):
  tiles = {}
  for i in range(0, len(game) - 2, 3):
    x = game[i]
    y = game[i + 1]
    tiles[(x, y)] = TILE_SYMBOLS[tile]
  for i in range(max_y+1):
    for j in range(max_x+1):
      print(tiles[(j, i)], end='')
    print()

# Part 1
print(block_count)

screen = {}
prog[0] = 2
comp = Intcode(prog.copy())

while True:
  move_input = input('Move (n, l, r): ')
  move = 0
  if move_input == 'l':
    move = -1
  elif move_input == 'r':
    move = 1

  s = comp.run(readin=[move], early_return=True, early_count=len(game) // 3)
  print_game(s)
