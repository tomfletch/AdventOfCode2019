#!/usr/bin/env python3
from __future__ import annotations
from typing import List, Set, Iterator
from dataclasses import dataclass
import math

ASTEROID_CHAR = '#'

def gcd(a: int, b: int) -> int:
    while b != 0:
        t = b
        b = a % b
        a = t
    return a

@dataclass(frozen=True)
class PolarPoint:
    angle: float
    magnitude: float

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

    def polar_coordinates(self):
        return PolarPoint(
            math.atan2(self.x, -self.y) % (2*math.pi),
            self.x*self.x + self.y*self.y
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

    def best_asteroid(self) -> Point:
        return max(self.asteroids, key=lambda a: self.visible_asteroids(a))

    def is_in_map(self, point: Point) -> bool:
        return (
            point.x >= 0 and point.x < self.width and
            point.y >= 0 and point.y < self.height
        )

    def sorted_asteroids(self, point: Point) -> Iterator[Point]:
        asteroids = [a for a in self.asteroids if a != point]

        asteroids = [(p, (p - point).polar_coordinates()) for p in asteroids]
        asteroids = sorted(asteroids, key=lambda a: (a[1].angle, a[1].magnitude))

        last_asteroid = None

        while asteroids:
            asteroid = asteroids.pop(0)
            if last_asteroid and last_asteroid != asteroid and last_asteroid[1].angle == asteroid[1].angle:
                asteroids.append(asteroid)
            else:
                yield asteroid[0]
            last_asteroid = asteroid


def main():
    map = read_map()
    best_asteroid = map.best_asteroid()
    sorted_asteroids = map.sorted_asteroids(best_asteroid)

    asteroid = None

    for _ in range(200):
        asteroid = next(sorted_asteroids)

    assert asteroid

    print('200th Asteroid:', asteroid)

    result = asteroid.x * 100 + asteroid.y
    print('Result:', result)

def read_map() -> Map:
    rows: List[List[bool]] = []

    with open('input.txt') as f:
        for line in f:
            rows.append([c == ASTEROID_CHAR for c in line.rstrip()])

    return Map(rows)


if __name__ == '__main__':
    main()
