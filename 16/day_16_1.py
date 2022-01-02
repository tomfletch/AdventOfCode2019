#!/usr/bin/env python3
from typing import List

PATTERN = [0,1,0,-1]

def main():
    signal = read_signal()
    patterns = calc_patterns(len(signal))

    for _ in range(100):
        signal = do_phase(signal, patterns)
    print(''.join(str(c) for c in signal[:8]))

def do_phase(signal: List[int], patterns: List[List[int]]) -> List[int]:
    new_signal: List[int] = []

    for i in range(len(signal)):
        digit_sum = 0
        for signal_digit, pattern_digit in zip(signal, patterns[i]):
            digit_sum += signal_digit * pattern_digit
        new_signal.append(abs(digit_sum) % 10)

    return new_signal


def calc_patterns(len: int) -> List[List[int]]:
    return [calc_pattern(len, i) for i in range(len)]

def calc_pattern(len: int, index: int) -> List[int]:
    pattern: List[int] = []
    for i in range(len):
        pattern.append(PATTERN[((i+1) // (index+1)) % 4])

    return pattern


def read_signal() -> List[int]:
    with open('input.txt') as f:
        return [int(c) for c in f.readline().rstrip()]

if __name__ == '__main__':
    main()
