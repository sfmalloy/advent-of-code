import fileinput
from collections import defaultdict
from copy import deepcopy

# defaultdict for the win, automatically sets new tiles to white.
tiles = defaultdict(bool)
WHITE = False
BLACK = True

# All the possible directions with changes in x and y for each. assuming.
# 
# Each hexagon has radius 2 rather than 1 to avoid use of floating point numbers.
# 
# Using zip with the different arrays came in handy and allowed me to more quickly
#   change values of DX and DY.
dirs = ['e','se','sw','w','nw','ne']
DX = {d:n for d,n in zip(dirs, [2,1,-1,-2,-1,1])}
DY = {d:n for d,n in zip(dirs, [0,-1,-1,0,1,1])}

for line in fileinput.input():
  line = line.strip()

  # While loop easier to use here than for loop with range because I can easily
  #   increase the index and add on to the direction without worry. Using a for
  #   loop with range makes this difficult.
  i = 0
  x = y = 0
  while i < len(line):
    d = line[i]
    if d in 'ns':
      i += 1
      d += line[i]
    x += DX[d]
    y += DY[d]
    i += 1
  tiles[(x,y)] = not tiles[(x,y)]

def tile_count(tiles):
  count = 0
  for color in tiles.values():
    if color == BLACK:
      count += 1
  return count

# Part 1 output
print(tile_count(tiles))

# Fill initial set of tiles with all neighbors of given tiles to ensure every tile
#   is in the initial state. Without this some tiles are missing making the final
#   count low.
filled = deepcopy(tiles)
for point,color in tiles.items():
  x,y = point
  if color == BLACK:
    for dx,dy in zip(DX.values(), DY.values()):
      if (x+dx,y+dy) not in filled:
        filled[(x+dx,y+dy)]
tiles = filled

# Simple cellular automata stuff, but this time no bounds checking because we have
#   a theoretically infinite hexagonal grid.
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

# Part 2 output
for i in range(100):
  tiles = do_day(tiles)
print(tile_count(tiles))