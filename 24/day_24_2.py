#!/usr/bin/env python3.11
from typing import Self

SIZE = 5

class Eris:
    state: int
    next_state: int
    level: int
    outer_eris: Self | None
    inner_eris: Self | None

    def __init__(self, state: int, level: int, outer_eris: Self | None = None, inner_eris: Self | None = None):
        self.state = state
        self.level = level

        self.outer_eris = outer_eris
        self.inner_eris = inner_eris

        if self.state != 0:
            if not self.outer_eris:
                self.outer_eris = Eris(0, level - 1, inner_eris = self)
            if not self.inner_eris:
                self.inner_eris = Eris(0, level + 1, outer_eris = self)

    def print_state(self):
        if self.level <= 0:
            if self.outer_eris:
                self.outer_eris.print_state()

        print(f'Depth {self.level}:')

        for y in range(5):
            output = ''
            for x in range(5):
                if x == 2 and y == 2:
                    output += '?'
                elif self.is_bug_at(x, y):
                    output += '#'
                else:
                    output += '.'
            print(output)
        print()

        if self.level >= 0:
            if self.inner_eris:
                self.inner_eris.print_state()

    def is_bug_at(self, x: int, y: int):
        if x < 0 or x >= SIZE: return False
        if y < 0 or y >= SIZE: return False

        bit_pos = y * SIZE + x
        return (self.state >> bit_pos) & 1 == 1

    def get_next_state(self):
        # Calculate next states

        if self.level <= 0 and self.outer_eris:
            self.outer_eris.get_next_state()

        self.next_state = 0
        for y in range(SIZE):
            for x in range(SIZE):
                if self.get_next_state_at(x, y):
                    bit_pos = y * SIZE + x
                    self.next_state |= 1 << bit_pos

        if self.level >= 0 and self.inner_eris:
            self.inner_eris.get_next_state()

        # Update all states
        if self.level <= 0 and self.outer_eris:
            self.outer_eris.update_state()

        if self.level >= 0 and self.inner_eris:
            self.inner_eris.update_state()

        if self.level == 0:
            self.update_state()

    def update_state(self):
        self.state = self.next_state

        if self.state != 0 and not self.inner_eris:
            self.inner_eris = Eris(0, self.level + 1, outer_eris=self)

        if self.state != 0 and not self.outer_eris:
            self.outer_eris = Eris(0, self.level - 1, inner_eris=self)

    def count_bugs_next_to(self, x: int, y: int, dx: int, dy: int):
        neighbour_x = x + dx
        neighbour_y = y + dy

        if neighbour_x == 2 and neighbour_y == 2 and self.inner_eris:
            total = 0

            if dx == 1:
                for inner_y in range(SIZE):
                    if self.inner_eris.is_bug_at(0, inner_y):
                        total += 1
            elif dx == -1:
                for inner_y in range(SIZE):
                    if self.inner_eris.is_bug_at(SIZE - 1, inner_y):
                        total += 1
            elif dy == 1:
                for inner_x in range(SIZE):
                    if self.inner_eris.is_bug_at(inner_x, 0):
                        total += 1
            elif dy == -1:
                for inner_x in range(SIZE):
                    if self.inner_eris.is_bug_at(inner_x, SIZE - 1):
                        total += 1

            return total

        if neighbour_x >= 0 and neighbour_x < SIZE and neighbour_y >= 0 and neighbour_y < SIZE:
            return int(self.is_bug_at(neighbour_x, neighbour_y))

        if not self.outer_eris:
            return 0

        if neighbour_x == -1:
            return int(self.outer_eris.is_bug_at(1, 2))

        if neighbour_x == SIZE:
            return int(self.outer_eris.is_bug_at(3, 2))

        if neighbour_y == -1:
            return int(self.outer_eris.is_bug_at(2, 1))

        if neighbour_y == SIZE:
            return int(self.outer_eris.is_bug_at(2, 3))

        raise Exception('Invalid state')


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
            self.count_bugs_next_to(x, y, -1, 0),
            self.count_bugs_next_to(x, y, 1, 0),
            self.count_bugs_next_to(x, y, 0, -1),
            self.count_bugs_next_to(x, y, 0, 1)
        ])

    def count_bugs(self) -> int:
        total = 0

        if self.level <= 0 and self.outer_eris:
            total += self.outer_eris.count_bugs()

        if self.level >= 0 and self.inner_eris:
            total += self.inner_eris.count_bugs()

        for y in range(SIZE):
            for x in range(SIZE):
                if x == 2 and y == 2: continue

                if self.is_bug_at(x, y):
                    total += 1

        return total


def main():
    state = read_state()
    eris = Eris(state, 0)

    # eris.print_state()

    # print('\nNext iteration\n')

    for _ in range(200):
        eris.get_next_state()

    eris.print_state()

    print('Total bugs:', eris.count_bugs())

    # states = set([state])

    # while True:
    #     eris.get_next_state()

    #     if eris.state not in states:
    #         states.add(eris.state)
    #     else:
    #         print('State appears twice:', eris.state)
    #         break



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
