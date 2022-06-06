#!/usr/bin/env python3
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Intcode import Computer, read_program

def main():
    program = read_program()
    computer = Computer(program, log_output=False)
    computer.run()
    output = ''

    while computer.outputs:
        output += chr(computer.get_output())

    output_lines = output.strip().split('\n')

    width = len(output_lines[0])
    height = len(output_lines)

    sum_alignment_params = 0

    for y in range(1, height-1):
        for x in range(1, width-1):
            if output_lines[y][x] == '#' and \
                    output_lines[y-1][x] == '#' and \
                    output_lines[y+1][x] == '#' and \
                    output_lines[y][x-1] == '#' and \
                    output_lines[y][x+1] == '#':
                sum_alignment_params += x * y

    print('Alignment Parameters Sum:', sum_alignment_params)

if __name__ == '__main__':
    main()
