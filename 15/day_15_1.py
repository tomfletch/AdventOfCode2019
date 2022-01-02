#!/usr/bin/env python3
from __future__ import annotations
from typing import Dict
from enum import Enum, IntEnum
from dataclasses import dataclass
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Intcode import Computer, read_program

class Direction(IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

class Tile(str, Enum):
    UNKNOWN = ' '
    WALL = '█'
    EMPTY = '.'
    OXYGEN_SYSTEM = 'X'

class DroidResponse(IntEnum):
    WALL = 0
    EMPTY = 1
    OXYGEN = 2

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Point):
        return Point(
            self.x + other.x,
            self.y + other.y
        )



class Droid:
    def __init__(self):
        self.position = Point(0,0)
        self.dist_to_point: Dict[Point, int] = {Point(0,0): 0}
        self.current_dist = 0

    def move(self, next_position: Point):
        if next_position in self.dist_to_point:
            self.current_dist = self.dist_to_point[next_position]
        else:
            self.current_dist += 1
            self.dist_to_point[next_position] = self.current_dist

        self.position = next_position

    def next_position(self, direction: Direction):
        if direction == Direction.NORTH:
            return self.position + Point(0, -1)
        if direction == Direction.SOUTH:
            return self.position + Point(0, 1)
        if direction == Direction.WEST:
            return self.position + Point(-1, 0)
        if direction == Direction.EAST:
            return self.position + Point(1, 0)


class Map:
    def __init__(self, droid: Droid):
        self.map: Dict[Point, Tile] = {}
        self.droid = droid
        self.set_tile(self.droid.position, Tile.EMPTY)

    def set_tile(self, point: Point, tile: Tile):
        self.map[point] = tile

    def __str__(self):
        output = ''

        x_min = min(p.x for p in self.map.keys())
        x_max = max(p.x for p in self.map.keys())
        y_min = min(p.y for p in self.map.keys())
        y_max = max(p.y for p in self.map.keys())

        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                p = Point(x,y)

                if p == self.droid.position:
                    output += 'D'
                elif p in self.map:
                    output += self.map[p].value
                else:
                    output += Tile.UNKNOWN.value
            output += '\n'

        return output


direction_order = [
    Direction.NORTH,
    Direction.EAST,
    Direction.SOUTH,
    Direction.WEST
]

def main():
    program = read_program()
    computer = Computer(program, log_output=False)

    droid = Droid()
    map = Map(droid)
    current_direction_index = 0

    while True:
        current_direction = direction_order[current_direction_index]
        next_position = droid.next_position(current_direction)
        computer.run([current_direction])
        response = DroidResponse(computer.get_output())

        if response == DroidResponse.EMPTY:
            current_direction_index = (current_direction_index - 1) % 4
            droid.move(next_position)
            map.set_tile(next_position, Tile.EMPTY)
        elif response == DroidResponse.WALL:
            map.set_tile(next_position, Tile.WALL)
            current_direction_index = (current_direction_index + 1) % 4
        elif response == DroidResponse.OXYGEN:
            droid.move(next_position)
            map.set_tile(next_position, Tile.OXYGEN_SYSTEM)
            break

        os.system('clear')
        print(map)
        print('Current distance:', droid.current_dist)

    print('Current distance:', droid.current_dist)




if __name__ == '__main__':
    main()
