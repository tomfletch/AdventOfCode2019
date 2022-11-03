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

    count_points = 0
    output = ''

    for y in range(50):
        for x in range(50):
            is_affected = test_beam_at(program, Point(x, y))

            if is_affected:
                output += '#'
                count_points += 1
            else:

                output += '.'

        output += '\n'

    print(output)
    print('Affected points:', count_points)


def test_beam_at(program: Program, point: Point):
    computer = Computer(program, log_output=False)
    computer.run([point.x, point.y])
    return computer.get_output() == 1


if __name__ == '__main__':
    main()
