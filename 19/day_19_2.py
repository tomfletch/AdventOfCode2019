#!/usr/bin/env python3
import os
import sys
from dataclasses import dataclass

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Intcode import Program, Computer, read_program

@dataclass
class Point:
    x: int
    y: int

def main():
    program = read_program()

    # Find starting points
    left_start_point = None
    right_start_point = None

    start_y = 10
    x = 0
    while not left_start_point or not right_start_point:
        this_point = Point(x, start_y)
        is_affected = test_beam_at(program, this_point)

        if not left_start_point and is_affected:
            left_start_point = this_point

        if left_start_point and not is_affected:
            this_point.x -= 1
            right_start_point = this_point

        x += 1

    # print(left_start_point)
    # print(right_start_point)

    left_point = left_start_point
    right_point = right_start_point

    while left_point.y - right_point.y + 1 < 100:
        left_point = get_next_left_point(program, left_point)
        # print(left_point)

    while right_point.x - left_point.x + 1 < 100:
        # print('Width:', right_point.x - left_point.x + 1)
        left_point = get_next_left_point(program, left_point)
        right_point = get_next_right_point(program, right_point)

    print(left_point)
    print(right_point)

    top_left = Point(left_point.x, right_point.y)
    print(top_left)

    print(top_left.x * 10000 + top_left.y)



def get_next_left_point(program: Program, point: Point):
    test_point = Point(point.x, point.y + 1)

    while not test_beam_at(program, test_point):
        test_point.x += 1

    return test_point

def get_next_right_point(program: Program, point: Point):
    test_point = Point(point.x + 1, point.y + 1)

    while test_beam_at(program, test_point):
        test_point.x += 1

    test_point.x -= 1
    return test_point



def test_beam_at(program: Program, point: Point):
    computer = Computer(program, log_output=False)
    computer.run([point.x, point.y])
    return computer.get_output() == 1


if __name__ == '__main__':
    main()
