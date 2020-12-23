import fileinput
from copy import deepcopy
from collections import namedtuple, deque

class Tile:
  def __init__(self, _id, tile):
    self.id = _id
    self.tile = tile
    self.angle = 0
  def next_orient(self):
    if self.angle == 3:
      self.flip_horiz()
    else:
      self.rotate_cw()
    self.angle += 1
  def rotate_cw(self):
    self.tile = list(map(list, zip(*self.tile)))
    self.flip_horiz()
  def flip_horiz(self):
    for i in range(len(self.tile)):
      a = 0
      b = len(self.tile)-1
      while a < b:
        t = self.tile[i][a]
        self.tile[i][a] = self.tile[i][b]
        self.tile[i][b] = t
        a += 1
        b -= 1
  def equal_rows(self, other):
    return self[-1] == other[0]
  def equal_cols(self, other):
    for i in range(len(self.tile)):
      if self[i][-1] != other[i][0]:
        return False
    return True
  def __getitem__(self, idx):
    return self.tile[idx]
  def __repr__(self):
    s = ''
    for r in self.tile:
      for c in r:
        s += c
      s += '\n'
    return s
  def combine_rows(self, other):
    new_tile = []
    for rs,ro in zip(self.tile, other.tile):
      new_tile.append(rs+ro)
    self.tile = new_tile
  def combine_cols(self, other):
    new_tile = self.tile + other.tile
    self.tile = new_tile
  def trim_borders(self):
    new_tile = []
    for r in self.tile[1:-1]:
      new_tile.append(r[1:-1])
    self.tile = new_tile

tiles = deque()
curr_id = 0
curr_tile = []
for line in fileinput.input():
  line = line.strip()
  if len(line) > 0:
    if line[0] == 'T':
      curr_id = int(line[:-1].split()[1])
      curr_tile = []
    else:
      curr_tile.append([c for c in line])
  else:
    new_tile = [[c for c in r] for r in curr_tile]
    t = Tile(curr_id, new_tile)
    for _ in range(8):
      tiles.append(deepcopy(t))
      t.next_orient()

grid_size = len(tiles) // 8
col_size = int(grid_size**(1/2))

node = namedtuple('node', 'row col grid ids')
frontier = deque()

for t in tiles:
  grid = [[None for _ in range(col_size)] for _ in range(col_size)]
  grid[0][0] = deepcopy(t)
  ids = {t.id}
  frontier.append(node(0, 0, grid, ids))

full_cols = set(col_size*i for i in range(1,col_size))

solved = None
while True:
  front = frontier.pop()
  if len(front.ids) < grid_size:
    for i in range(len(tiles)):
      if tiles[i].id not in front.ids:
        valid = True
        if len(front.ids) < col_size or len(front.ids) not in full_cols:
          valid = front.grid[front.row][front.col].equal_rows(tiles[i])
        if valid:
          row = front.row + 1
          col = front.col
          if row > col_size-1:
            row = 0
            col = front.col + 1
          if col > 0:
            valid = front.grid[row][col-1].equal_cols(tiles[i])
          if valid:
            grid_copy = deepcopy(front.grid)
            grid_copy[row][col] = deepcopy(tiles[i])
            frontier.append(node(row, col, grid_copy, front.ids | {tiles[i].id}))
  else:
    solved = front.grid
    break
# Part 1 answer
prod = solved[0][0].id * solved[0][-1].id * solved[-1][0].id * solved[-1][-1].id
print(prod)

#####################################################################################
# Start of part 2

# Combine the tiles into a mega-tile aka image because you'll need to reorient it most likely
for i in range(len(solved)):
  for j in range(len(solved)):
    solved[i][j].trim_borders()

trimmed = Tile(0, [])
for i in range(len(solved)):
  for j in range(1, len(solved)):
    solved[i][0].combine_rows(solved[i][j])
  trimmed.combine_cols(solved[i][0])

trimmed.rotate_cw()
trimmed.rotate_cw()
trimmed.rotate_cw()
print(trimmed)