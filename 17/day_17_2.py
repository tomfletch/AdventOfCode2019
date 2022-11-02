#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
import os
import sys
from typing import List

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Intcode import Computer, read_program

class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @staticmethod
    def turn_right(dir: Direction):
        return Direction((int(dir) + 1) % 4)

    @staticmethod
    def turn_left(dir: Direction):
        return Direction((int(dir) - 1) % 4)


EMPTY_CHAR = '.'
WALL_CHAR = '#'

DIRECTION_CHARS = {
    '^': Direction.UP,
    '>': Direction.RIGHT,
    'v': Direction.DOWN,
    '<': Direction.LEFT
}

@dataclass
class Robot:
    x: int
    y: int
    direction: Direction


class Map:
    grid: List[List[str]]
    robot: Robot

    def __init__(self, map_str: str):
        self.grid = [list(line) for line in map_str.split('\n')]
        self.width = len(self.grid[0])
        self.height = len(self.grid)
        self.find_robot()
        print(self.robot)

    def find_robot(self):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]

                if cell in DIRECTION_CHARS:
                    direction = DIRECTION_CHARS[cell]
                    self.robot = Robot(x, y, direction)
                    self.grid[y][x] = WALL_CHAR

    def get_cell(self, x: int, y: int):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return EMPTY_CHAR

        return self.grid[y][x]

    def get_next_position(self, direction: Direction):
        next_x = self.robot.x
        next_y = self.robot.y

        if direction == Direction.UP:
            next_y -= 1
        elif direction == Direction.DOWN:
            next_y += 1
        elif direction == Direction.RIGHT:
            next_x += 1
        elif direction == Direction.LEFT:
            next_x -= 1

        return (next_x, next_y)

    def get_next_cell(self, direction: Direction):
        next_x, next_y = self.get_next_position(direction)
        return self.get_cell(next_x, next_y)

    def get_next_move(self):
        if self.get_next_cell(self.robot.direction) == WALL_CHAR:
            next_x, next_y = self.get_next_position(self.robot.direction)
            self.robot.x = next_x
            self.robot.y = next_y
            return 'F'

        new_direction = Direction.turn_left(self.robot.direction)
        if self.get_next_cell(new_direction) == WALL_CHAR:
            self.robot.direction = new_direction
            return 'L'

        new_direction = Direction.turn_right(self.robot.direction)
        if self.get_next_cell(new_direction) == WALL_CHAR:
            self.robot.direction = new_direction
            return 'R'

        return None

    def __str__(self):
        output = ''

        for y, line in enumerate(self.grid):
            for x, char in enumerate(line):
                if self.robot.y == y and self.robot.x == x:
                    for char, dir in DIRECTION_CHARS.items():
                        if dir == self.robot.direction:
                            output += char
                            break
                else:
                    output += char
            output += '\n'

        return output

def main():
    program = read_program()
    program[0] = 2

    computer = Computer(program, log_output=False)
    computer.run()

    output = ''

    while output[-2:] != '\n\n':
        output += chr(computer.get_output())

    map = Map(output.strip())
    print(map)

    moves: List[str] = []

    next_move = map.get_next_move()
    forward_count = 0

    while next_move:

        if next_move == 'F':
            forward_count += 1
        else:
            if forward_count != 0:
                moves.append(str(forward_count))
                forward_count = 0

            moves.append(next_move)

        next_move = map.get_next_move()

    if forward_count != 0:
        moves.append(str(forward_count))


    print_computer_text(computer)

    computer.run(str_to_ascii('A,B,A,C,A,B,C,B,C,B\n'))

    print_computer_text(computer)

    computer.run(str_to_ascii('L,10,R,8,L,6,R,6\n'))

    print_computer_text(computer)

    computer.run(str_to_ascii('L,8,L,8,R,8\n'))

    print_computer_text(computer)

    computer.run(str_to_ascii('R,8,L,6,L,10,L,10\n'))

    print_computer_text(computer)

    computer.run(str_to_ascii('n\n'))

    output = ''

    while output[-2:] != '\n\n':
        output += chr(computer.get_output())

    print(computer.get_output())

def print_computer_text(computer: Computer):
    output = ''
    while computer.outputs:
        output += chr(computer.get_output())
    print(output)

def str_to_ascii(s: str):
    return [ord(c) for c in s]



if __name__ == '__main__':
    main()
