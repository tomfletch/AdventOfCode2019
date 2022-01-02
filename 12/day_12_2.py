#!/usr/bin/env python3
from __future__ import annotations
import re
from typing import List, Tuple, Set, NamedTuple
from dataclasses import dataclass

def gcd(a: int, b: int) -> int:
    while b != 0:
        t = b
        b = a % b
        a = t
    return a

def lcm(a: int, b: int) -> int:
    return (a * b) // gcd(a,b)

class Vector(NamedTuple):
    x: int
    y: int
    z: int

@dataclass(frozen=True)
class Moon:
    position: int
    velocity: int

    def move(self):
        return Moon(
            self.position + self.velocity,
            self.velocity
        )


class System:
    def __init__(self, moons: List[Moon]):
        self.time_step = 0
        self.moons = moons

    def step(self):
        self.time_step += 1
        self.apply_gravity()
        self.apply_velocity()

    def apply_gravity(self):
        for moon_1_index in range(len(self.moons)):
            for moon_2_index in range(moon_1_index+1, len(self.moons)):
                self.apply_gravity_between(moon_1_index, moon_2_index)

    def apply_gravity_between(self, moon_1_index: int, moon_2_index: int):
        moon_1 = self.moons[moon_1_index]
        moon_2 = self.moons[moon_2_index]
        delta = self.compare_position(moon_1.position, moon_2.position)

        self.moons[moon_1_index] = Moon(moon_1.position, moon_1.velocity + delta)
        self.moons[moon_2_index] = Moon(moon_2.position, moon_2.velocity - delta)

    def compare_position(self, a: int, b: int) -> int:
        if a < b:
            return 1
        if a > b:
            return -1
        return 0

    def apply_velocity(self):
        for moon_index, moon in enumerate(self.moons):
            self.moons[moon_index] = moon.move()

    def get_state(self) -> Tuple[Moon, ...]:
        return tuple(self.moons)


def main():
    moon_positions = read_moon_positions()

    steps = 1

    for axis in range(3):
        moons = [Moon(m[axis], 0) for m in moon_positions]
        system = System(moons)

        system_states: Set[Tuple[Moon, ...]] = set()
        system_state = system.get_state()

        while system_state not in system_states:
            system_states.add(system_state)
            system.step()
            system_state = system.get_state()

        steps = lcm(steps, system.time_step)

    print(f'Steps:', steps)

def read_moon_positions() -> List[Vector]:
    with open('input.txt') as f:
        return [parse_vector(l) for l in f]


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
