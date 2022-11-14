#!/usr/bin/env python3.11

BASE_PATTERN = [0, 1, 0, -1]

def main():
    signal = read_input()
    for _ in range(100):
        signal = fft(signal)
    print(''.join(str(x) for x in signal[:8]))

def fft(signal: list[int]):
    output: list[int] = []

    for i in range(len(signal)):
        output.append(fft_digit(i, signal))

    return output

def fft_digit(digit: int, signal: list[int]):
    total = 0
    for i in range(digit, len(signal)):
        mult = BASE_PATTERN[((i + 1) // (digit + 1)) % 4]
        total += mult * signal[i]

    return abs(total) % 10

def read_input():
    with open('input.txt') as file:
        return [int(x) for x in file.readline().strip()]

if __name__ == '__main__':
    main()
