#!/usr/bin/env python3
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Intcode import Computer, read_program

def main():
    program = read_program()
    program[1] = 12
    program[2] = 2
    computer = Computer(program)
    computer.run()
    value = computer.read_at(0)
    print(f'Value at position 0: {value}')

if __name__ == '__main__':
    main()
