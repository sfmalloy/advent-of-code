import fileinput

actions = fileinput.input()

# Constants
dx = [0,1,0,-1]
dy = [1,0,-1,0]
c = {90:0, 180:-1, 270:0}
s = {90:1, 180:0, 270:-1}
dirs = {d:n for n,d in enumerate('NESW')}

# Part 1 functions
def move(x, y, direction, dist):
  x += dist * dx[direction]
  y += dist * dy[direction]
  return x, y

def rotate_ship(curr_dir, direction, angle):
  if direction == 'L':
    angle *= -1
  return (curr_dir + (angle // 90)) % 4

# Part 2 functions
def rotate_waypoint(wx, wy, direction, angle):
  if direction == 'R':
    if angle == 90:
      angle = 270
    elif angle == 270:
      angle = 90
  return wx*c[angle] - wy*s[angle], wx*s[angle] + wy*c[angle]

def move_relative(x, y, wx, wy, dist):
  x += dist * wx
  y += dist * wy
  return x, y

x1 = y1 = x2 = y2 = 0
curr_dir = dirs['E']
wx = 10
wy = 1
for a in actions:
  action = a[0]
  dist = int(a[1:])
  if action in dirs:
    x1, y1 = move(x1, y1, dirs[action], dist)
    wx, wy = move(wx, wy, dirs[action], dist)
  elif action == 'F':
    x1, y1 = move(x1, y1, curr_dir, dist)
    x2, y2 = move_relative(x2, y2, wx, wy, dist)
  elif action in 'LR':
    curr_dir = rotate_ship(curr_dir, action, dist)
    wx, wy = rotate_waypoint(wx, wy, action, dist)

print(abs(x1)+abs(y1))
print(abs(x2)+abs(y2))