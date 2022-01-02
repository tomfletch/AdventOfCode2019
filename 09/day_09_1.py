#!/usr/bin/env python3
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Intcode import Computer, read_program

def main():
    program = read_program()
    computer = Computer(program)
    computer.run([1])


if __name__ == '__main__':
    main()
