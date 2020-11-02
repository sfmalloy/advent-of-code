X = 0
Y = 1
Z = 2

class moon:
  def __init__(self, x, y, z):
    self.pos = [x, y, z]
    self.vel = [0, 0, 0]
  def csv_line_pos(self):
    return f'{self.pos[X]},{self.pos[Y]},{self.pos[Z]},'
  def __str__(self):
    return f'pos=<x= {self.pos[X]}, y= {self.pos[Y]}, z= {self.pos[Z]}>, vel=<x= {self.vel[X]}, y= {self.vel[Y]}, z= {self.vel[Z]}>'
  def __repr__(self):
    return str(self)
  def __copy__(self):
    return moon(self.pos[X], self.pos[Y], self.pos[Z])
  def copy(self):
    return self.__copy__()

def do_step(moons):
  # Apply gravity
  for i in range(len(moons)):
    for j in range(i, len(moons)):
      for k in range(3):
        if moons[i].pos[k] < moons[j].pos[k]:
          moons[i].vel[k] += 1
          moons[j].vel[k] -= 1
        elif moons[i].pos[k] > moons[j].pos[k]:
          moons[i].vel[k] -= 1
          moons[j].vel[k] += 1
  
  # Apply velocity
  for m in moons:
    for i in range(3):
      m.pos[i] += m.vel[i]

moons = []
moonsx = []
moonsy = []
moonsz = []
with open('12.in', 'r') as readfile:
  lines = [line[1:-2].split(', ') for line in readfile.readlines()]
  for l in lines:
    x, y, z = map(lambda s: int(s.split('=')[1]), l)
    moons.append(moon(x, y, z))
    moonsx.append(moon(x, y, z))
    moonsy.append(moon(x, y, z))
    moonsz.append(moon(x, y, z))

f = open('plots.csv', 'w')

STEPS = 1000
for i in range(STEPS):
  do_step(moons)

print(sum(sum(abs(p) for p in m.pos) * sum(abs(v) for v in m.vel) for m in moons))

def find_cycle(moons, axis):
  init_pos = [m.pos[axis] for m in moons]
  init_vel = [m.vel[axis] for m in moons]
  cycle = 1
  do_step(moons)
  while [m.pos[axis] for m in moons] != init_pos or [m.vel[axis] for m in moons] != init_vel:
    do_step(moons)
    cycle += 1

  return cycle

def gcd(a, b):
  if b == 0:
    return a
  return gcd(b, a % b)

def lcm(a, b):
  return a * b // gcd(a, b)

# Each cycle is independent
x_cycle = find_cycle(moonsx, X)
y_cycle = find_cycle(moonsy, Y)
z_cycle = find_cycle(moonsz, Z)

print(lcm(x_cycle, lcm(y_cycle, z_cycle)))