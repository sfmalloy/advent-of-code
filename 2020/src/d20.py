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

monster_mid = '#    ##    ##    ###'
orientations = []
mx = 0
for o in range(8):
  good_count = 0
  good_coords = []
  for r in range(1, len(trimmed.tile)-1):
    i = 0
    while i < len(trimmed.tile)-len(monster_mid):
      sub_row = trimmed[r][i:i+len(monster_mid)]
      sadge = False
      for c,s,m in zip(range(len(monster_mid)), sub_row, monster_mid):
        if m != ' ' and s != m:
          sadge = True
          break
      if not sadge:
        good_count += 1
        good_coords.append((r,i))
        i += 20
      else:
        i += 1
  if good_count > 0:
    orientations.append((o, good_count, good_coords, deepcopy(trimmed)))
    mx = max(mx, good_count)
  trimmed.next_orient()
trimmed.next_orient()

monster_counts = []
for orient in orientations:
  monster_count = 0
  if orient[1] == mx:
    for r,c in orient[2]:
      valid = True
      top = orient[3][r-1][c+18]
      if top == '#':
        bot = orient[3][r+1][c:c+20]
        for check_char in [1,4,7,10,13,16]:
          if bot[check_char] != '#':
            valid = False
            break
      else:
        valid = False
      if valid:
        monster_count += 1
  monster_counts.append(monster_count)
print(monster_counts)

count = max(monster_counts)

tile_count = 0
for r in trimmed:
  for c in r:
    tile_count += c == '#'

print(tile_count - (count * 15))
