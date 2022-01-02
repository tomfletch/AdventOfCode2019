#!/usr/bin/env python3
from enum import IntEnum
from typing import NamedTuple, Dict, Optional
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

    def __str__(self) -> str:
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

    def ball_position(self) -> Point:
        position = self.find_tile_position(TileType.BALL)
        assert position
        return position

    def paddle_position(self) -> Point:
        position = self.find_tile_position(TileType.HORIZONTAL_PADDLE)
        assert position
        return position

    def find_tile_position(self, tile_type: TileType) -> Optional[Point]:
        for point, point_tile_type in self.grid.items():
            if tile_type == point_tile_type:
                return point
        return None


class Game:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.score = 0

    def set_score(self, score: int):
        self.score = score

    def __str__(self) -> str:
        output = str(self.grid)
        output += '\n'
        output += f'Score: {self.score}'
        return output


def main():
    program = read_program()
    program[0] = 2
    computer = Computer(program, log_output=False)
    computer.run()


    grid = Grid()
    game = Game(grid)

    while True:

        while computer.outputs:
            x = computer.get_output()
            y = computer.get_output()

            if x == -1 and y == 0:
                new_score = computer.get_output()
                game.set_score(new_score)
            else:
                tile_type = TileType(computer.get_output())
                grid.set_tile(Point(x,y), tile_type)

        if computer.halted:
            break

        if computer.waiting_for_input:
            ball_position = grid.ball_position()
            paddle_position = grid.paddle_position()

            if ball_position.x < paddle_position.x:
                joystick = -1
            elif ball_position.x > paddle_position.x:
                joystick = 1
            else:
                joystick = 0

            computer.run([joystick])

        os.system('clear')
        print(game)

    os.system('clear')
    print(game)


if __name__ == '__main__':
    main()
