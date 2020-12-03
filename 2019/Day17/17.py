from intcode import Intcode
from collections import namedtuple

with open('17.in') as f:
  prog = list(map(int, f.readline().split(',')))
comp = Intcode(prog)

screen_ascii = comp.run()
screen = []
line = ''
for s in screen_ascii:
  if s != 10:
    line += chr(s)
  elif len(line) > 0:
    screen.append(line)
    line = ''

x = y = 0
p1 = 0
for i in range(1, len(screen)-1):
  for j in range(1, len(screen[i])-1):
    if screen[i][j] == '#':
      if screen[i-1][j] == screen[i+1][j] == screen[i][j-1] == screen[i][j+1] == screen[i][j]:
        p1 += i*j
    
print(p1)

tile_count = 0
for i in range(len(screen)):
  for j in range(len(screen[i])):
    tile_count += screen[i][j] == '#'
    if screen[i][j] == '^':
      bot_x = j
      bot_y = i

prog[0] = 2
comp = Intcode(prog)

N = 0
E = 1
S = 2
W = 3
bot_dirs = dict(zip('^>v<', [N,E,S,W]))

def turn(curr, d):
  if d == 'R':
    return (curr+1) % (W+1)
  return (curr-1) % (W+1)

def step(screen, x, y, do_move=True):
  old_x = x
  old_y = y
  bot = screen[y][x]
  d = bot_dirs[bot]
  if d == N:
    y -= 1
  elif d == E:
    x += 1
  elif d == S:
    y += 1
  else:
    x -= 1
  if 0 <= y < len(screen) and 0 <= x < len(screen[0]) and screen[y][x] != '.':
    if do_move:
      screen[old_y][old_x] = 'O'
      screen[y][x] = bot
    return True
  return False

def can_move(screen, x, y):
  bots = '^>v<'
  bot = screen[y][x]
  valid = [False for _ in range(4)]
  valid_count = 0
  for _ in range(4):
    screen[y][x] = bots[turn(bot_dirs[bot], 'R')]
    bot = screen[y][x]
    valid[bot_dirs[bot]] = step(screen, x, y, False)
    valid_count += valid[bot_dirs[bot]]
  if valid[bot_dirs[bot]]:
    return True
  elif valid_count == 1:
    return valid[(bot_dirs[bot]+1)%4] or valid[(bot_dirs[bot]+3)%4]

test_screen = [[c for c in line] for line in screen]
# find the path while you are able to move