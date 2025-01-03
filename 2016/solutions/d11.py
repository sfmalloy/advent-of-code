import re
from io import TextIOWrapper
from dataclasses import dataclass
from collections import deque


@dataclass
class Container:
    floor: int
    microchips: frozenset[str]
    generators: frozenset[str]


def main(file: TextIOWrapper):
    floors1 = []
    floors2 = []
    for f, line in enumerate(file.readlines()):
        microchips = re.findall(r'([^ ]+)-compatible microchip', line)
        generators = re.findall(r'([^ ]+) generator', line)
        floors1.append(Container(f, frozenset(microchips), frozenset(generators)))
        floors2.append(Container(f, frozenset(microchips), frozenset(generators)))
    return part2(floors2), 0


def part1(init_layout: list[Container]):
    return get_min_path(init_layout)


def part2(init_layout: list[Container]):
    init_layout[0].generators |= frozenset({'elerium', 'dilithium'})
    init_layout[0].microchips |= frozenset({'elerium', 'dilithium'})
    return get_min_path(init_layout)


def get_min_path(init_layout: list[Container]):
    top_floor_number = 3
    q = deque([(Container(0, frozenset(), frozenset()), init_layout, 0)])
    visited = set()
    while q:
        elevator, floors, steps = q.popleft()
        # 0. check if we're at the goal state. if we are, return
        if elevator.floor == top_floor_number:
            valid = True
            for f in floors[:-1]:
                if f.generators or f.microchips:
                    valid = False
            if valid:
                return steps
        v = generate_visited_key(elevator, floors)
        if v in visited:
            continue
        visited.add(v)

        floors[elevator.floor].microchips |= elevator.microchips
        floors[elevator.floor].generators |= elevator.generators

        for a in floors[elevator.floor].microchips:
            floors[elevator.floor].microchips -= {a}
            if elevator.floor + 1 < len(floors):
                append_if_valid(q, (Container(elevator.floor + 1, {a}, frozenset()), [Container(f.floor, f.microchips, f.generators) for f in floors], steps + 1))
            if elevator.floor - 1 >= 0:
                append_if_valid(q, (Container(elevator.floor - 1, {a}, frozenset()), [Container(f.floor, f.microchips, f.generators) for f in floors], steps + 1))

            for b in floors[elevator.floor].microchips:
                floors[elevator.floor].microchips -= {b}
                if elevator.floor + 1 < len(floors):
                    append_if_valid(q, (Container(elevator.floor + 1, {a, b}, frozenset()), [Container(f.floor, f.microchips, f.generators) for f in floors], steps + 1))
                floors[elevator.floor].microchips |= {b}
            floors[elevator.floor].microchips |= {a}


        for a in floors[elevator.floor].generators:
            floors[elevator.floor].generators -= {a}
            if elevator.floor + 1 < len(floors):
                append_if_valid(q, (Container(elevator.floor + 1, frozenset(), {a}), [Container(f.floor, f.microchips, f.generators) for f in floors], steps + 1))
            if elevator.floor - 1 >= 0:
                append_if_valid(q, (Container(elevator.floor - 1, frozenset(), {a}), [Container(f.floor, f.microchips, f.generators) for f in floors], steps + 1))

            for b in floors[elevator.floor].generators:
                floors[elevator.floor].generators -= {b}
                if elevator.floor + 1 < len(floors):
                    append_if_valid(q, (Container(elevator.floor + 1, frozenset(), {a, b}), [Container(f.floor, f.microchips, f.generators) for f in floors], steps + 1))
                floors[elevator.floor].generators |= {b}
            floors[elevator.floor].generators |= {a}


        for a in floors[elevator.floor].microchips:
            floors[elevator.floor].microchips -= {a}
            for b in floors[elevator.floor].generators:
                floors[elevator.floor].generators -= {b}
                if elevator.floor + 1 < len(floors):
                    append_if_valid(q, (Container(elevator.floor + 1, {a}, {b}), [Container(f.floor, f.microchips, f.generators) for f in floors], steps + 1))
                floors[elevator.floor].generators |= {b}
            floors[elevator.floor].microchips |= {a}


def validate_floor_state(elevator: Container, floors: list[Container]):
    for f in floors:
        generators = f.generators
        microchips = f.microchips
        if f.floor == elevator.floor:
            generators |= elevator.generators
            microchips |= elevator.microchips
        if not generators or not microchips:
            continue
        for m in microchips:
            if m not in generators:
                return False
    return True


def generate_visited_key(elevator: Container, floors: list[Container]):
    visited = []
    for f in floors:
        generators = f.generators
        microchips = f.microchips
        if f.floor == elevator.floor:
            generators |= elevator.generators
            microchips |= elevator.microchips
        visited.append((generators, microchips))
    return (elevator.floor, *visited)


def append_if_valid(q, state):
    if validate_floor_state(state[0], state[1]):
        q.append(state)
