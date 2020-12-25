import fileinput
from collections import namedtuple, defaultdict

point3d = namedtuple('point3d', 'x y z')
point4d = namedtuple('point4d', 'x y z w')
cubes = defaultdict(bool)
hypercubes = defaultdict(bool)

max_x = max_y = 0
for y, line in enumerate(fileinput.input()):
  line = line.strip()
  for x, state in enumerate(line):
    cubes[point3d(x,y,0)] = state == '#'
  max_y = y
  max_x = len(line)

for x in range(-1, max_x+2):
  for y in range(-1, max_y+2):
    for z in range(-1,2):
      cubes[point3d(x,y,z)]

for pos,state in cubes.items():
  for w in range(-1,2):
    pos4d = point4d(pos.x, pos.y, pos.z, w)
    hypercubes[pos4d] = state and w == 0

def cycle3(cubes):
  new_cubes = cubes.copy()
  for pos,state in cubes.items():
    active_count = 0
    for x in range(pos.x-1, pos.x+2):
      for y in range(pos.y-1, pos.y+2):
        for z in range(pos.z-1, pos.z+2):
          neighbor = point3d(x,y,z)
          if neighbor != pos and (neighbor in cubes and cubes[neighbor]):
            active_count += 1
          else:
            new_cubes[neighbor]
    if state:
      new_cubes[pos] = active_count == 2 or active_count == 3
    else:
      new_cubes[pos] = active_count == 3
  return new_cubes

def cycle4(cubes):
  new_cubes = cubes.copy()
  for pos,state in cubes.items():
    active_count = 0
    for x in range(pos.x-1, pos.x+2):
      for y in range(pos.y-1, pos.y+2):
        for z in range(pos.z-1, pos.z+2):
          for w in range(pos.w-1, pos.w+2):
            neighbor = point4d(x,y,z,w)
            if neighbor != pos and (neighbor in cubes and cubes[neighbor]):
              active_count += 1
            else:
              new_cubes[neighbor]
    if state:
      new_cubes[pos] = active_count == 2 or active_count == 3
    else:
      new_cubes[pos] = active_count == 3
  return new_cubes

CYCLES = 6
for _ in range(CYCLES):
  cubes = cycle3(cubes)

active = 0
for state in cubes.values():
  active += state
print(active)

for _ in range(CYCLES):
  hypercubes = cycle4(hypercubes)

active = 0
for state in hypercubes.values():
  active += state
print(active)
