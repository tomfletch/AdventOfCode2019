#!/usr/bin/env python3
from typing import Tuple
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Intcode import Computer, read_program, Program

def main():
    program = read_program()
    noun, verb = find_noun_verb(program)
    result = 100 * noun + verb
    print(f'Noun: {noun}')
    print(f'Verb: {verb}')
    print(f'Result: {result}')

def find_noun_verb(program: Program) -> Tuple[int, int]:
    for noun in range(100):
        for verb in range(100):
            computer = Computer(program.copy())
            computer.write_at(1, noun)
            computer.write_at(2, verb)
            computer.run()
            value = computer.read_at(0)

            if value == 19690720:
                return noun, verb

    raise RuntimeError('Did not find noun and verb')

if __name__ == '__main__':
    main()
