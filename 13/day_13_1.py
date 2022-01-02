#!/usr/bin/env python3
from enum import IntEnum
from typing import NamedTuple, Dict
from collections import defaultdict
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Intcode import Computer, read_program

class TileType(IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    HORIZONTAL_PADDLE = 3
    BALL = 4

TILE_CHARS = {
    TileType.EMPTY: ' ',
    TileType.WALL: '█',
    TileType.BLOCK: '▒',
    TileType.HORIZONTAL_PADDLE: '▀',
    TileType.BALL: 'O'
}

class Point(NamedTuple):
    x: int
    y: int

class Grid:
    def __init__(self):
        self.grid: Dict[Point, TileType] = defaultdict(lambda: TileType.EMPTY)

    def set_tile(self, point: Point, tile_type: TileType):
        self.grid[point] = tile_type

    def __str__(self):
        output = ''

        x_max = max(p.x for p in self.grid)
        y_max = max(p.y for p in self.grid)

        for y in range(0, y_max + 1):
            for x in range(0, x_max + 1):
                tile_type = self.grid[Point(x,y)]
                output += TILE_CHARS[tile_type]
            output += '\n'
        return output

    def count_of_type(self, tile_type: TileType) -> int:
        return list(self.grid.values()).count(tile_type)

def main():
    program = read_program()
    computer = Computer(program, log_output=False)
    computer.run()


    grid = Grid()

    while computer.outputs:
        x = computer.get_output()
        y = computer.get_output()
        tile_type = TileType(computer.get_output())
        grid.set_tile(Point(x,y), tile_type)

    print(grid)
    print('Block tiles:', grid.count_of_type(TileType.BLOCK))

if __name__ == '__main__':
    main()
