from dataclasses import dataclass
from math import sqrt
from typing import Any, Self


@dataclass(frozen=True, eq=True, order=True)
class Vec2:
    x_or_r: int
    y_or_c: int

    @property
    def x(self):
        return self.x_or_r

    @property
    def y(self):
        return self.y_or_c

    @property
    def r(self):
        return self.x_or_r

    @property
    def c(self):
        return self.y_or_c

    @x.setter
    def x(self, v) -> None:
        self.x_or_r = v

    @y.setter
    def y(self, v) -> None:
        self.y_or_c = v

    @r.setter
    def r(self, v) -> None:
        self.x_or_r = v

    @c.setter
    def c(self, v) -> None:
        self.y_or_c = v

    def __add__(self, other: Self):
        return Vec2(self.x_or_r + other.x_or_r, self.y_or_c + other.y_or_c)

    def __sub__(self, other: Self):
        return Vec2(self.x_or_r - other.x_or_r, self.y_or_c - other.y_or_c)

    def __mul__(self, other: int):
        return Vec2(self.x_or_r * other, self.y_or_c * other)

    def __rmul__(self, other: int):
        return self.__mul__(other)

    def __mod__(self, other: int):
        return Vec2(self.x_or_r % other, self.y_or_c % other)

    def __truediv__(self, other: float):
        if not (isinstance(other, (int, float))):
            return NotImplemented
        return Vec2(self.x_or_r / other, self.y_or_c / other)

    def __floordiv__(self, other: float):
        if not (isinstance(other, (int, float))):
            return NotImplemented
        return Vec2(self.x_or_r // other, self.y_or_c // other)

    def dot(self, other: Self):
        if not isinstance(other, Vec2):
            return NotImplemented
        return self.x_or_r * other.x_or_r + self.y_or_c * other.y_or_c

    def cross(self, other: Self):
        if not isinstance(other, Vec2):
            return NotImplemented
        return self.x_or_r * other.y_or_c - self.y_or_c * other.x_or_r

    def distance(self, other: Self) -> float:
        if not isinstance(other, Vec2):
            return NotImplemented
        return sqrt((self.x_or_r - other.x_or_r) ** 2 + (self.y_or_c - other.y_or_c) ** 2)

    def manhattan_distance(self, other: Self):
        if not isinstance(other, Vec2):
            return NotImplemented
        return abs(self.x_or_r - other.x_or_r) + abs(self.y_or_c - other.y_or_c)

    def magnitude(self):
        return sqrt(self.dot(self))

    def normalized(self):
        return self / self.magnitude()

    def in_bounds_xy(
        self, grid: list[list[Any]], lower_limit_x=0, lower_limit_y=0, upper_limit_x=None, upper_limit_y=None
    ):
        """
        NOTE: limits are `[lower, upper)`
        """
        return (
            self.x >= lower_limit_x
            and self.y >= lower_limit_y
            and self.x < (upper_limit_x if upper_limit_x else len(grid[self.y]))
            and self.y < (upper_limit_y if upper_limit_y else len(grid))
        )

    def in_bounds_rc(
        self, grid: list[list[Any]], lower_limit_r=0, lower_limit_c=0, upper_limit_r=None, upper_limit_c=None
    ):
        """
        NOTE: limits are `[lower, upper)`
        """
        return (
            self.r >= lower_limit_r
            and self.c >= lower_limit_c
            and self.r < (upper_limit_r if upper_limit_r else len(grid))
            and self.c < (upper_limit_c if upper_limit_c else len(grid[self.r]))
        )

    def __repr__(self) -> str:
        return f'({self.x_or_r}, {self.y_or_c})'


class XYDir:
    N = Vec2(0, 1)
    S = Vec2(0, -1)
    E = Vec2(1, 0)
    W = Vec2(-1, 0)

    L = W
    R = E
    U = N
    D = S

    _opposite = frozendict({N: S, S: N, E: W, W: E})

    ALL = frozendict({N, S, E, W})

    @staticmethod
    def opposite(d: Self):
        return XYDir._opposite[d]


class RCDir:
    N = Vec2(-1, 0)
    S = Vec2(1, 0)
    E = Vec2(0, 1)
    W = Vec2(0, -1)

    L = W
    R = E
    U = N
    D = S

    _opposite = frozendict({N: S, S: N, E: W, W: E})

    _clockwise = frozendict({N: E, E: S, S: W, W: N})

    _counter_clockwise = frozendict({N: W, W: S, S: E, E: N})

    ALL = frozenset([N, S, E, W])

    @staticmethod
    def opposite(d: Self):
        return RCDir._opposite[d]

    @staticmethod
    def clockwise(src: Vec2):
        return RCDir._clockwise[src]

    @staticmethod
    def counter_clockwise(src: Vec2):
        return RCDir._counter_clockwise[src]
