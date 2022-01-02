#!/usr/bin/env python3
from __future__ import annotations
from typing import List, Set
from dataclasses import dataclass

ASTEROID_CHAR = '#'

def gcd(a: int, b: int) -> int:
    while b != 0:
        t = b
        b = a % b
        a = t
    return a

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __sub__(self, other: Point):
        return Point(
            self.x - other.x,
            self.y - other.y
        )

    def __add__(self, other: Point):
        return Point(
            self.x + other.x,
            self.y + other.y
        )

    def __repr__(self):
        return f'({self.x},{self.y})'

    def simplified(self):
        divisor = abs(gcd(self.x, self.y))
        return Point(
            self.x // divisor,
            self.y // divisor
        )

class Map:
    def __init__(self, map: List[List[bool]]):
        self.width = len(map[0])
        self.height = len(map)
        self.asteroids: Set[Point] = set()

        for y, row in enumerate(map):
            for x, cell in enumerate(row):
                if cell:
                    self.asteroids.add(Point(x,y))

    def visible_asteroids(self, asteroid: Point) -> int:
        visible_asteroids = self.asteroids.copy()
        visible_asteroids.remove(asteroid)

        for other_asteroid in self.asteroids:
            if other_asteroid == asteroid:
                continue

            delta = other_asteroid - asteroid
            delta = delta.simplified()

            check_position = other_asteroid + delta

            while self.is_in_map(check_position):
                visible_asteroids.discard(check_position)
                check_position += delta

        return len(visible_asteroids)

    def max_visible_asteroids(self) -> int:
        return max(self.visible_asteroids(a) for a in self.asteroids)

    def is_in_map(self, point: Point) -> bool:
        return (
            point.x >= 0 and point.x < self.width and
            point.y >= 0 and point.y < self.height
        )



def main():
    map = read_map()
    max_visible_asteroids = map.max_visible_asteroids()
    print('Max visible asteroids:', max_visible_asteroids)

def read_map() -> Map:
    rows: List[List[bool]] = []

    with open('input.txt') as f:
        for line in f:
            rows.append([c == ASTEROID_CHAR for c in line.rstrip()])

    return Map(rows)


if __name__ == '__main__':
    main()
