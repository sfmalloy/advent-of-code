import fileinput
from collections import namedtuple, deque
from copy import deepcopy
from math import sqrt
from time import sleep

class Tile:
  def __init__(self, _id, image):
    self.id = _id
    self.image = image
  def __repr__(self):
    return str(self)
  def __str__(self):
    s = ''
    for r in self.image:
      s += ''.join(r) + '\n'
    return s
  def __len__(self):
    return len(self.image)
  def flip_horiz(self):
    i = 0
    j = len(self.image)-1
    while i < j:
      for k in range(len(self.image)):
        temp = self.image[k][i]
        self.image[k][i] = self.image[k][j]
        self.image[k][j] = temp
      i += 1
      j -= 1
  def rotate(self):
    self.image = list(map(list, zip(*self.image)))
    self.flip_horiz()
  def __getitem__(self, row):
    return self.image[row]
  def get_edges(self):
    top_row = self.image[0]
    bot_row = self.image[-1]
    right_col = []
    left_col = []
    for r in range(len(self.image)):
      left_col.append(self.image[r][0])
      right_col.append(self.image[r][-1])
    return (top_row, right_col, bot_row, left_col)
  def compare_edges(self, other):
    self_edges = self.get_edges()
    other_edges = other.get_edges()
    equal = set()
    for i in range(len(self_edges)):
      for j in range(len(other_edges)):
        if self_edges[i] == other_edges[j]:
          equal.add((i,j))
    return equal
class Grid:
  def __init__(self, rows, cols):
    self.grid = [[]]
    self.rows = rows
    self.cols = cols
    self.curr_row = 0
    self.curr_col = -1
    self.ids = set()
  def __len__(self):
    return sum(len(row) for row in self.grid)
  def __repr__(self):
    return str(self)
  def __str__(self):
    s = ''
    for i in range(self.rows):
      for r in range(len(self.grid[0][0])):
        for j in range(self.cols):
          try:
            s += ''.join(self.grid[i][j][r]) + ' '
          except IndexError:
            break
        s += '\n'
      s += '\n'
    return s
  def __getitem__(self, idx):
    return self.grid[idx]
  def add(self, tile):
    if self.curr_col == self.cols-1:
      self.curr_row += 1
      self.curr_col = -1
      self.grid.append([])
    self.grid[self.curr_row].append(tile)
    self.curr_col += 1
    self.ids.add(tile.id)
  def get_curr_tile(self):
    return self.grid[self.curr_row][self.curr_col]

tiles = deque()
curr_tile = []
curr_id = 0
for line in fileinput.input():
  line = line.strip()
  if len(line) == 0:
    tiles.append(Tile(curr_id, curr_tile))
    curr_tile = []
  elif line[0] == 'T':
    curr_id = int(line.split()[1][:-1])
  else:
    curr_tile.append([c for c in line.strip()])

grid_len = int(sqrt(len(tiles)))
grid_total = len(tiles)

frontier = deque()

all_tiles = deque()
init = Grid(grid_len, grid_len)
for i in range(len(tiles)):
  for j in range(8):
    init_copy = deepcopy(init)
    if j > 0:
      if j == 4:
        tiles[i].flip_horiz()
      else:
        tiles[i].rotate()
    init_copy.add(deepcopy(tiles[i]))
    frontier.append(init_copy)
    all_tiles.append(deepcopy(tiles[i]))
  tiles.append(tiles.popleft())

solved = None
front = None
valid = False
while not valid:
  front = frontier.pop()
  for i in range(len(all_tiles)):
    if all_tiles[i].id not in front.ids:
      if (1, 3) in front.get_curr_tile().compare_edges(all_tiles[i]) or len(front[front.curr_row]) == front.cols:
        front_copy = deepcopy(front)
        front_copy.add(deepcopy(all_tiles[i]))
        if front_copy.curr_row == 0 or (0, 2) in all_tiles[i].compare_edges(front_copy[front_copy.curr_row-1][front_copy.curr_col]):
          frontier.append(front_copy)
          if len(front_copy) == grid_total:
            valid = True
            solved = front_copy
            break
prod = solved[0][0].id * solved[0][-1].id * solved[-1][0].id * solved[-1][-1].id
print(prod)
print(solved)