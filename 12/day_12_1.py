#!/usr/bin/env python3
from __future__ import annotations
import re
from typing import List

class Vector:
    def __init__(self, x: int, y: int, z: int):
        self.v = (x, y, z)

    def energy(self) -> int:
        return sum(abs(v) for v in self.v)

    def __getitem__(self, axis: int) -> int:
        return self.v[axis]

    def __iadd__(self, other: Vector):
        self.v = [s + o for (s, o) in zip(self.v, other.v)]
        return self

    def __isub__(self, other: Vector):
        self.v = [s - o for (s, o) in zip(self.v, other.v)]
        return self

    def __repr__(self) -> str:
        return str(self.v)


class Moon:
    def __init__(self, position: Vector):
        self.position = position
        self.velocity = Vector(0,0,0)

    def move(self):
        self.position += self.velocity

    def total_energy(self) -> int:
        return self.position.energy() * self.velocity.energy()

    def __repr__(self):
        return f'Moon(p={self.position}, v={self.velocity})'


class System:
    def __init__(self, moons: List[Moon]):
        self.time_step = 0
        self.moons = moons

    def step(self):
        self.apply_gravity()
        self.apply_velocity()

    def apply_gravity(self):
        for moon_1_index, moon_1 in enumerate(self.moons):
            for moon_2 in self.moons[moon_1_index+1:]:
                self.apply_gravity_between(moon_1, moon_2)

    def apply_gravity_between(self, moon_1: Moon, moon_2: Moon):
        delta = [0,0,0]
        for axis in range(3):
            delta[axis] = self.compare_position(moon_1.position[axis], moon_2.position[axis])

        delta = Vector(delta[0], delta[1], delta[2])

        moon_1.velocity += delta
        moon_2.velocity -= delta

    def compare_position(self, a: int, b: int) -> int:
        if a < b:
            return 1
        if a > b:
            return -1
        return 0

    def apply_velocity(self):
        for moon in self.moons:
            moon.move()

    def total_energy(self) -> int:
        return sum(moon.total_energy() for moon in self.moons)


def main():
    moons = read_moons()
    system = System(moons)

    for _ in range(1000):
        system.step()

    print('Total energy:', system.total_energy())


def read_moons() -> List[Moon]:
    with open('input.txt') as f:
        return [Moon(parse_vector(l)) for l in f]


def parse_vector(vector_str: str) -> Vector:
    # <x=-8, y=0, z=4>
    match = re.match(r'<x=(?P<x>-?\d+), y=(?P<y>-?\d+), z=(?P<z>-?\d+)>', vector_str)
    assert match

    return Vector(
        int(match.group('x')),
        int(match.group('y')),
        int(match.group('z'))
    )


if __name__ == '__main__':
    main()
