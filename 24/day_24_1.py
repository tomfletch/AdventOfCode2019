#!/usr/bin/env python3.11

SIZE = 5

class Eris:
    state: int

    def __init__(self, state: int):
        self.state = state

    def print_state(self):
        for y in range(5):
            output = ''
            for x in range(5):
                if self.is_bug_at(x, y):
                    output += '#'
                else:
                    output += '.'
            print(output)

    def is_bug_at(self, x: int, y: int):
        if x < 0 or x >= SIZE: return False
        if y < 0 or y >= SIZE: return False

        bit_pos = y * SIZE + x
        return (self.state >> bit_pos) & 1 == 1

    def get_next_state(self):
        next_state = 0

        for y in range(SIZE):
            for x in range(SIZE):
                if self.get_next_state_at(x, y):
                    bit_pos = y * SIZE + x
                    next_state |= 1 << bit_pos

        self.state = next_state

    def get_next_state_at(self, x: int, y: int):
        is_bug = self.is_bug_at(x, y)
        neighbours = self.count_neighbours(x, y)

        if is_bug and neighbours != 1:
            return False

        if not is_bug and (neighbours == 1 or neighbours == 2):
            return True

        return is_bug

    def count_neighbours(self, x: int, y: int):
        return sum([
            self.is_bug_at(x-1, y),
            self.is_bug_at(x+1, y),
            self.is_bug_at(x, y-1),
            self.is_bug_at(x, y+1),
        ])


def main():
    state = read_state()
    eris = Eris(state)

    states = set([state])

    while True:
        eris.get_next_state()

        if eris.state not in states:
            states.add(eris.state)
        else:
            print('State appears twice:', eris.state)
            break



def read_state():
    state = 0
    shift_bits = 0

    with open('input.txt') as file:
        for line in file:
            for chr in line:
                if chr == '#':
                    state |= 1 << shift_bits
                    shift_bits += 1
                elif chr == '.':
                    shift_bits += 1

    return state


if __name__ == '__main__':
    main()
