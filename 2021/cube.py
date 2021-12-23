from dataclasses import dataclass

@dataclass
class Cube:
    x_min: int
    x_max: int

    y_min: int
    y_max: int

    z_min: int
    z_max: int

c1 = Cube(10,12+1,10,12+1,10,12+1)
c2 = Cube(1,3,1,3,1,3)

dx = max(min(c1.x_max, c2.x_max) - max(c1.x_min, c2.x_min), 0)
dy = max(min(c1.y_max, c2.y_max) - max(c1.y_min, c2.y_min), 0)
dz = max(min(c1.z_max, c2.z_max) - max(c1.z_min, c2.z_min), 0)

print(dx * dy * dz)
