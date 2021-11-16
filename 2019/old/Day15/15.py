from intcode import Intcode
from collections import namedtuple
from copy import deepcopy
from time import sleep

with open('15.in') as rf:
  prog = list(map(int, rf.readline().rstrip().split(',')))
  comp = Intcode(prog)

N = 1
S = 2
W = 3
E = 4

dx = [0,0,1,-1]
dy = [1,-1,0,0]

def move(c, m):
  return c.run(readin=[m], early_return=True)[0]

def opposite(m):
  if m == N:
    return S
  elif m == S:
    return N
  elif m == W:
    return E
  else:
    return W

node = namedtuple('node', 'x y status path robot')
point = namedtuple('point', 'x y')

known = {}
frontier = [node(0, 0, 1, [], comp)]
curr = frontier.pop(0)

while curr.status != 2:
  if point(curr.x, curr.y) not in known:
    known[point(curr.x, curr.y)] = curr.status

  for i in range(N, E+1):
    p = point(curr.x+dx[i-1], curr.y+dy[i-1])
    bot = deepcopy(curr.robot)
    m = move(bot, i)
    if p not in known and m != 0:
      frontier.append(node(p.x, p.y, m, curr.path+[i], bot))
    elif m == 0:
      known[point(p.x, p.y)] = m
  curr = frontier.pop()
  print(curr.path)

print(len(curr.path))
min_x = min(known, key=lambda p: p.x).x
min_y = min(known, key=lambda p: p.y).y
max_x = max(known, key=lambda p: p.x).x
max_y = max(known, key=lambda p: p.y).y

def print_maze(known):
  for y in range(min_y, max_y+1):
    for x in range(min_x, max_x+1):
      p = point(x, y)
      if p in known:
        if known[p] == 0:
          print('#', end='')
        elif known[p] == 1:
          print(' ', end='')
        else:
          print('O', end='')
      else:
        print('#', end='')
    print()


edges = [[point(curr.x, curr.y)]]
t = 0
while 1 in set(p[1] for p in known.items()):
  front = edges.pop(0)
  adj = []
  for f in front:
    x = f.x
    y = f.y
    for d in range(N, E+1):
      p = point(x+dx[d-1], y+dy[d-1])
      if p in known and known[p] == 1:
        known[p] = 2
        adj.append(p)
  edges.append(adj)
  t += 1

print(t)