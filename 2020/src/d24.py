import fileinput
from collections import defaultdict
from copy import deepcopy

lines = [l.strip() for l in fileinput.input()]

tiles = defaultdict(bool)
WHITE = False
BLACK = True

dirs = ['e','se','sw','w','nw','ne']
DX = {d:n for d,n in zip(dirs, [2,1,-1,-2,-1,1])}
DY = {d:n for d,n in zip(dirs, [0,-1,-1,0,1,1])}

first = True
for l in lines:
  i = 0
  x = y = 0
  while i < len(l):
    d = l[i]
    if d in 'ns':
      i += 1
      d += l[i]
    x += DX[d]
    y += DY[d]
    i += 1
  tiles[(x,y)] = not tiles[(x,y)]

filled = deepcopy(tiles)
for point,color in tiles.items():
  x,y = point
  if color == BLACK:
    for dx,dy in zip(DX.values(), DY.values()):
      if (x+dx,y+dy) not in filled:
        filled[(x+dx,y+dy)]
tiles = filled

def tile_count(day):
  count = 0
  for color in day.values():
    if color == BLACK:
      count += 1
  return count

print(tile_count(tiles))

def do_day(curr_day):
  next_day = deepcopy(curr_day)
  for point,color in curr_day.items():
    x,y = point
    black_tiles = 0
    for dx,dy in zip(DX.values(), DY.values()):
      neighbor = (x+dx,y+dy)
      if neighbor not in curr_day:
        next_day[neighbor] = WHITE
      elif curr_day[neighbor] == BLACK:
        black_tiles += 1
    if color == BLACK and (black_tiles == 0 or black_tiles > 2):
      next_day[point] = WHITE
    elif color == WHITE and black_tiles == 2:
      next_day[point] = BLACK
  return next_day


for i in range(100):
  tiles = do_day(tiles)
print(tile_count(tiles))