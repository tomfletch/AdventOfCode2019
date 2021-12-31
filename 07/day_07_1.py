#!/usr/bin/env python3
import os
import sys
from itertools import permutations

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Intcode import Computer, read_program


def main():
    program = read_program()

    max_signal = 0

    for settings in permutations([0,1,2,3,4]):

        signal = 0

        for phase_setting in settings:
            amplifier = Computer(program.copy())
            amplifier.run([phase_setting, signal])
            assert amplifier.output is not None
            signal = amplifier.output

        if signal > max_signal:
            max_signal = signal

    print('Max signal:', max_signal)

if __name__ == '__main__':
    main()
