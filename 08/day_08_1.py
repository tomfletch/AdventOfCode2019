#!/usr/bin/env python3
from typing import List, TypeVar, Iterator
import math

class Image:
    def __init__(self, data: List[int]):
        self.data = data
        self.width = 25
        self.height = 6
        self.layer_size = self.width * self.height
        self.layers = chunks(self.data, self.layer_size)


def main():
    image = read_image()

    fewest_zeros = math.inf
    layer_with_fewest_zeros = None

    for layer in image.layers:
        layer_zeros = count_digit(layer, 0)

        if layer_zeros < fewest_zeros:
            fewest_zeros = layer_zeros
            layer_with_fewest_zeros = layer

    assert layer_with_fewest_zeros

    layer_ones = count_digit(layer_with_fewest_zeros, 1)
    layer_twos = count_digit(layer_with_fewest_zeros, 2)
    result = layer_ones * layer_twos
    print('Result:', result)


def count_digit(layer: List[int], digit: int) -> int:
    return sum(1 if d == digit else 0 for d in layer)


T = TypeVar('T')

def chunks(lst: List[T], n: int) -> Iterator[List[T]]:
    for i in range(0, len(lst), n):
        yield lst[i:i+n]


def read_image() -> Image:
    with open('input.txt') as f:
        return Image([int(c) for c in f.read().rstrip()])

if __name__ == "__main__":
    main()
