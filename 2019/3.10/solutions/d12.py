from io import TextIOWrapper

class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
        return f'<x={self.x}, y={self.y}, z={self.z}>'
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

class Moon:
    def __init__(self, init_pos: Vector):
        self.pos = init_pos
        self.vel = Vector()
    
    def move(self):
        self.pos += self.vel
    
    def get_energy(self):
        pot = abs(self.pos.x) + abs(self.pos.y) + abs(self.pos.z)
        kin = abs(self.vel.x) + abs(self.vel.y) + abs(self.vel.z)
        return pot * kin
    
    def __repr__(self):
        return f'pos: {self.pos}, vel: {self.vel}'

    def __eq__(self, other):
        return self.pos == other.pos and self.vel == other.vel

def sign(n):
    if n < 0:
        return -1
    elif n > 0:
        return 1
    return 0

def main(in_file: TextIOWrapper):
    moons_a = []
    moons_b = []
    for l in in_file.readlines():
        moons_a.append(Moon(Vector(*(int(c.split('=')[-1]) for c in l.strip()[1:-1].split(',')))))
        moons_b.append(Moon(Vector(*(int(c.split('=')[-1]) for c in l.strip()[1:-1].split(',')))))
    
    moons = moons_a
    for _ in range(1000):
        for i in range(len(moons)):
            for j in range(len(moons)):
                if i != j:
                    diff = moons[j].pos - moons[i].pos
                    moons[i].vel += Vector(sign(diff.x), sign(diff.y), sign(diff.z))
        for m in moons:
            m.move()
    print(sum([m.get_energy() for m in moons]))
