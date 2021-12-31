#!/usr/bin/env python3
from typing import Dict, Set

class OrbitMap:
    def __init__(self):
        self.orbiting: Dict[str, str] = {}

    def add_orbit(self, object_1: str, object_2: str):
        self.orbiting[object_2] = object_1

    def get_orbit_set(self, obj: str) -> Set[str]:
        current = obj
        orbit_set: Set[str] = set()

        while current != 'COM':
            current = self.orbiting[current]
            orbit_set.add(current)

        return orbit_set


def main():
    orbit_map = read_orbit_map()
    orbit_set_you = orbit_map.get_orbit_set('YOU')
    orbit_set_san = orbit_map.get_orbit_set('SAN')

    not_in_common = orbit_set_you ^ orbit_set_san
    transfers = len(not_in_common)
    print('Transfers:', transfers)


def read_orbit_map() -> OrbitMap:
    orbit_map = OrbitMap()

    with open('input.txt') as f:
        for line in f:
            object_1, object_2 = line.rstrip().split(')')
            orbit_map.add_orbit(object_1, object_2)

    return orbit_map


if __name__ == '__main__':
    main()
