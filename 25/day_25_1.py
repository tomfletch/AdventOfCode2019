#!/usr/bin/env python3.11
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Intcode import Computer, read_program

def main():
    program = read_program()

    computer = Computer(program, log_output=False)
    computer.run()

    print(computer.get_ascii_output())

    while True:
        command = input()
        computer.run(command.strip() + '\n')
        print(computer.get_ascii_output())


if __name__ == '__main__':
    main()
