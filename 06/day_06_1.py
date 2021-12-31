#!/usr/bin/env python3
from typing import Dict, List, Tuple
from collections import defaultdict

class OrbitMap:
    def __init__(self):
        self.orbiters: Dict[str, List[str]] = defaultdict(list)

    def add_orbit(self, object_1: str, object_2: str):
        self.orbiters[object_1].append(object_2)

    def count_orbits(self, obj: str) -> Tuple[int, int]:
        if len(self.orbiters[obj]) == 0:
            return 0, 0

        count = 0
        total_children = 0

        for orbiter in self.orbiters[obj]:
            child_orbits, child_children = self.count_orbits(orbiter)
            count += 1 + child_children + child_orbits
            total_children += child_children + 1

        return count, total_children

def main():
    orbit_map = read_orbit_map()
    (count,_) = orbit_map.count_orbits('COM')
    print(f'Count of orbits: {count}')

def read_orbit_map() -> OrbitMap:
    orbit_map = OrbitMap()

    with open('input.txt') as f:
        for line in f:
            object_1, object_2 = line.rstrip().split(')')
            orbit_map.add_orbit(object_1, object_2)

    return orbit_map


if __name__ == '__main__':
    main()
