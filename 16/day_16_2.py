#!/usr/bin/env python3.11

def main():
    signal = read_input() * 10000
    position = int(''.join(str(x) for x in signal[:7]))
    signal = signal[position:]
    for i in range(100):
        print('Iteration:', i)
        signal = fft(signal)
    print(''.join(str(x) for x in signal[:8]))

def fft(signal: list[int]):
    output: list[int] = []

    total = 0

    for i in range(len(signal)):
        total += signal[len(signal) - i - 1]
        output.append(total % 10)

    return output[::-1]


def read_input():
    with open('input.txt') as file:
        return [int(x) for x in file.readline().strip()]

if __name__ == '__main__':
    main()
