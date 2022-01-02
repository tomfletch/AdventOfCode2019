#!/usr/bin/env python3
from __future__ import annotations
from typing import Set
from enum import IntEnum
from dataclasses import dataclass
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Intcode import Computer, read_program

class Color(IntEnum):
    BLACK = 0
    WHITE = 1

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Point) -> Point:
        return Point(
            self.x + other.x,
            self.y + other.y
        )

class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

DIRECTION_VECTORS = {
    Direction.UP:    Point(0,1),
    Direction.RIGHT: Point(1,0),
    Direction.DOWN:  Point(0,-1),
    Direction.LEFT:  Point(-1,0)
}

class Rotation(IntEnum):
    LEFT = 0
    RIGHT = 1


class Hull:
    def __init__(self):
        self.map: Set[Point] = set()
        self.painted: Set[Point] = set()

    def set_color(self, point: Point, color: Color):
        self.painted.add(point)
        if color == Color.WHITE:
            self.map.add(point)
        elif color == Color.BLACK:
            self.map.discard(point)

    def get_color(self, point: Point):
        if point in self.map:
            return Color.WHITE
        return Color.BLACK

    def __str__(self) -> str:
        output = ''

        x_min = min(p.x for p in self.map)
        x_max = max(p.x for p in self.map)
        y_min = min(p.y for p in self.map)
        y_max = max(p.y for p in self.map)

        for y in range(y_max, y_min - 1, -1):
            for x in range(x_min, x_max + 1):
                if Point(x,y) in self.map:
                    output += '#'
                else:
                    output += ' '

            output += '\n'

        return output


class Robot:
    def __init__(self, hull: Hull):
        self.hull = hull
        self.direction = Direction.UP
        self.position = Point(0,0)

    def paint(self, color: Color):
        self.hull.set_color(self.position, color)

    def detect_color(self):
        return self.hull.get_color(self.position)

    def rotate(self, rotate: Rotation):
        if rotate == Rotation.LEFT:
            direction_delta = -1
        elif rotate == Rotation.RIGHT:
            direction_delta = 1

        self.direction = Direction((self.direction + direction_delta) % 4)

    def move_forward(self):
        self.position += DIRECTION_VECTORS[self.direction]


def main():
    program = read_program()
    computer = Computer(program, log_output=False)

    hull = Hull()
    hull.set_color(Point(0,0), Color.WHITE)
    robot = Robot(hull)

    computer.run([robot.detect_color()])

    while not computer.halted:
        color = Color(computer.get_output())
        rotation = Rotation(computer.get_output())

        robot.paint(color)
        robot.rotate(rotation)
        robot.move_forward()

        computer.run([robot.detect_color()])

    print(hull)

if __name__ == '__main__':
    main()
