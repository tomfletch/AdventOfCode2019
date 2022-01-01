#!/usr/bin/env python3
from typing import List, TypeVar, Iterator
import math
from enum import IntEnum

class Color(IntEnum):
    BLACK = 0
    WHITE = 1
    TRANSPARENT = 2

COLOR_CHAR = {
    Color.WHITE: '#',
    Color.BLACK: ' ',
    Color.TRANSPARENT: '?'
}

class Image:
    def __init__(self, data: List[int]):
        self.data = data
        self.width = 25
        self.height = 6
        self.layer_size = self.width * self.height
        self.layers = chunks(self.data, self.layer_size)

    def render(self) -> List[Color]:
        result = [Color.TRANSPARENT] * self.layer_size

        for layer in self.layers:
            for i, color in enumerate(layer):
                if result[i] == Color.TRANSPARENT:
                    result[i] = Color(color)

        return result


def main():
    image = read_image()

    output = image.render()

    for y in range(image.height):
        row = ''
        for x in range(image.width):
            color = output[y*image.width + x]
            row += COLOR_CHAR[color]
        print(row)

T = TypeVar('T')

def chunks(lst: List[T], n: int) -> Iterator[List[T]]:
    for i in range(0, len(lst), n):
        yield lst[i:i+n]


def read_image() -> Image:
    with open('input.txt') as f:
        return Image([int(c) for c in f.read().rstrip()])

if __name__ == "__main__":
    main()
