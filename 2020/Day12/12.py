from math import cos, sin, radians

with open('12.in') as f:
  actions = f.readlines()

dx = [0,1,0,-1]
dy = [1,0,-1,0]
dirs = {a:b for b,a in enumerate('NESW')}

# Part 1
def move(x, y, direction, dist):
  x += dist * dx[direction]
  y += dist * dy[direction]
  return x, y

def rotate_ship(curr_dir, direction, angle):
  if direction == 'L':
    angle *= -1
  curr_dir += angle // 90
  curr_dir %= 4
  return curr_dir

x = y = 0
curr_dir = dirs['E']
for a in actions:
  cmd = a[0]
  dist = int(a[1:])
  if cmd in dirs:
    x, y = move(x, y, dirs[cmd], dist)
  elif cmd == 'F':
    x, y = move(x, y, curr_dir, dist)
  elif cmd in 'LR':
    curr_dir = rotate_ship(curr_dir, cmd, dist)

print(abs(x)+abs(y))

# Part 2
def rotate_waypoint(d, angle, wx, wy):
  if d == 'R':
    if angle == 90:
      angle = 270
    elif angle == 270:
      angle = 90
  angle = radians(angle)
  c = int(cos(angle))
  s = int(sin(angle))

  new_wx = wx*c - wy*s
  new_wy = wx*s + wy*c

  return new_wx, new_wy

def move_relative(x, y, wx, wy, dist):
  x += dist * wx
  y += dist * wy
  return x, y

x = y = 0
wx = 10
wy = 1
for a in actions:
  cmd = a[0]
  dist = int(a[1:])
  if cmd in dirs:
    wx, wy = move(wx, wy, dirs[cmd], dist)
  elif cmd == 'F':
    x, y = move_relative(x, y, wx, wy, dist)
  elif cmd in 'LR':
    wx, wy = rotate_waypoint(cmd, dist, wx, wy)

print(abs(x)+abs(y))
