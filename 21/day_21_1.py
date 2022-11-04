#!/usr/bin/env python3

import os
import sys

os.system('clear')

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Intcode import Computer, read_program

def main():
    program = read_program()
    computer = Computer(program, log_output=False)
    computer.run()
    print(computer.get_ascii_output())

    springscript = [
        'NOT A T',
        'NOT B J',
        'OR T J',
        'NOT C T',
        'OR T J',
        'AND D J',
        'WALK'
    ]

    computer.run('\n'.join(springscript) + '\n')

    print(computer.get_ascii_output())


if __name__ == '__main__':
    main()
