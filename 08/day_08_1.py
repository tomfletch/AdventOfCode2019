#!/usr/bin/env python3
from typing import List, TypeVar, Iterator

class Image:
    def __init__(self, data: List[int]):
        self.data = data
        self.width = 25
        self.height = 6
        self.layer_size = self.width * self.height
        self.layers = chunks(self.data, self.layer_size)


def main():
    image = read_image()
    layer_with_fewest_zeros = min(image.layers, key=lambda l: l.count(0))
    layer_ones = layer_with_fewest_zeros.count(1)
    layer_twos = layer_with_fewest_zeros.count(2)
    result = layer_ones * layer_twos
    print('Result:', result)


T = TypeVar('T')

def chunks(lst: List[T], n: int) -> Iterator[List[T]]:
    for i in range(0, len(lst), n):
        yield lst[i:i+n]


def read_image() -> Image:
    with open('input.txt') as f:
        return Image([int(c) for c in f.read().rstrip()])

if __name__ == "__main__":
    main()
