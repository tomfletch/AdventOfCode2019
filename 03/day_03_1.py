#!/usr/bin/env python3
from __future__ import annotations
from typing import NamedTuple, List, Tuple, Set
from enum import Enum
from dataclasses import dataclass

class Direction(str, Enum):
    UP = 'U'
    RIGHT = 'R'
    DOWN = 'D'
    LEFT = 'L'

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Point):
        return Point(
            self.x + other.x,
            self.y + other.y
        )

class Vector(NamedTuple):
    direction: Direction
    magnitude: int

    def delta(self) -> Point:
        return {
            Direction.UP:    Point(0,1),
            Direction.RIGHT: Point(1,0),
            Direction.DOWN:  Point(0,-1),
            Direction.LEFT:  Point(-1,0),
        }[self.direction]

    def __repr__(self) -> str:
        return f'{self.direction.value}{self.magnitude}'

Wire = List[Vector]

def find_closest_intersection(wire_1: Wire, wire_2: Wire) -> int:
    wire_1_points = get_wire_points(wire_1)
    wire_2_points = get_wire_points(wire_2)

    crossing_points = wire_1_points.intersection(wire_2_points)

    origin = Point(0,0)
    crossing_distances = [manhattan_distance(origin, c) for c in crossing_points]
    return min(crossing_distances)

def get_wire_points(wire: Wire) -> Set[Point]:
    points: Set[Point] = set()

    pos = Point(0,0)

    for vector in wire:

        delta = vector.delta()

        for _ in range(vector.magnitude):
            pos += delta
            points.add(pos)

    return points

def manhattan_distance(point_1: Point, point_2: Point) -> int:
    return abs(point_2.x - point_1.x) + abs(point_2.y - point_1.y)

def main():
    wire_1, wire_2 = read_wires()
    distance = find_closest_intersection(wire_1, wire_2)
    print(f'Distance: {distance}')

def read_wires() -> Tuple[Wire, Wire]:
    with open('input.txt') as f:
        wire_1 = parse_wire(f.readline().rstrip())
        wire_2 = parse_wire(f.readline().rstrip())

    return wire_1, wire_2

def parse_wire(line: str) -> Wire:
    parts = line.split(',')
    return [parse_vector(p) for p in parts]

def parse_vector(v: str) -> Vector:
    d = Direction(v[0])
    m = int(v[1:])
    return Vector(d, m)

if __name__ == '__main__':
    main()
