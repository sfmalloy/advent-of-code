from lib import advent
from lib.common.vec import Vec3
from io import TextIOWrapper
from collections import deque, defaultdict
from dataclasses import dataclass
from typing import Self

@dataclass(init=False)
class Particle:
    pos: Vec3
    vel: Vec3
    acc: Vec3
    hit: bool = False

    def __init__(self, p: str, v: str, a: str):
        self.pos = self._parse(p)
        self.vel = self._parse(v)
        self.acc = self._parse(a)

        self.prev_pos = self.pos

    def _parse(self, vs: str):
        return Vec3(*map(int, vs[3:-1].split(',')))
    
    def step(self):
        self.vel += self.acc
        self.prev_pos = self.pos
        self.pos += self.vel
    
    def away_state(self):
        return (
            self.state_check(self.pos.x, self.vel.x, self.acc.x)
            and self.state_check(self.pos.y, self.vel.y, self.acc.y)
            and self.state_check(self.pos.z, self.vel.z, self.acc.z)
        )

    def state_check(self, p, v, a):
        return (
            (self._sign(p) == self._sign(v) or self._sign(v) == 0) 
            and (self._sign(a) == 0 or self._sign(a) == self._sign(v))
        )

    
    def _sign(self, a: int):
        if a == 0:
            return 0
        return abs(a) // a
    

    def getting_closer(self, other: Self):
        return (not self.hit) and (self.pos.manhattan_distance(other.pos) <= self.prev_pos.manhattan_distance(other.prev_pos))


@advent.parser(20)
def parse(file: TextIOWrapper):
    return [Particle(*line.strip().split(', ')) for line in file.readlines()]


@advent.solver(20, part=1)
def solve1(particles: list[Particle]):
    while not all(p.away_state() for p in particles):
        for p in particles:
            p.step()

    best = float('inf')
    index = 0
    for i, p in enumerate(particles):
        if p.pos.manhattan_distance(Vec3(0, 0, 0)) < best:
            best = p.pos.manhattan_distance(Vec3(0, 0, 0))
            index = i
    return index


@advent.solver(20, part=2)
def solve2(particles: list[Particle]):
    steady = False
    while not steady:
        steady = True
        for p in particles:
            if not p.hit:
                p.step()
        for i, a in enumerate(particles):
            for b in particles[i+1:]:
                if a.pos == b.pos:
                    a.hit = True
                    b.hit = True
                elif a.getting_closer(b):
                    steady = False
    return len(particles) - sum(p.hit for p in particles)
