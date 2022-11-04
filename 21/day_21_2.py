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

    # springscript = [
    #     'OR A J',
    #     'AND B J',
    #     'AND C J',
    #     'NOT J J',
    #     'AND D J',
    #     'WALK'
    # ]

    springscript = [
        'OR E T',
        'AND F T',
        'OR H T',
        'OR E J',
        'AND I J',
        'OR J T',
        'NOT A J',
        'NOT J J',
        'AND B J',
        'AND C J',
        'NOT J J',
        'AND D J',
        'AND T J',
        'RUN'
    ]

    computer.run('\n'.join(springscript) + '\n')

    print(computer.get_ascii_output())


if __name__ == '__main__':
    main()
