#!/usr/bin/env python3
from typing import List
import os
import sys
from itertools import permutations

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Intcode import Computer, read_program


def main():
    program = read_program()

    max_signal = 0

    for settings in permutations([5,6,7,8,9]):

        amplifiers: List[Computer] = []

        for phase_setting in settings:
            amplifier = Computer(program.copy())
            amplifier.run([phase_setting])
            amplifiers.append(amplifier)

        signal = 0
        current_amplifier = 0
        while not amplifiers[-1].halted:
            amplifier = amplifiers[current_amplifier]
            amplifier.run([signal])
            assert amplifier.output is not None
            signal = amplifier.output
            current_amplifier = (current_amplifier + 1) % len(amplifiers)

        if signal > max_signal:
            max_signal = signal

    print('Max signal:', max_signal)

if __name__ == '__main__':
    main()
