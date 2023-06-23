#!/usr/bin/env python3.11
DECK_SIZE = 119315717514047
POSITION = 2020

def main():
    instructions = read_instructions()
    card_position = POSITION

    hit_positions = {card_position}

    for i in range(101741582076661):
        if i % 100000 == 0:
            print(i)

        for instruction in reversed(instructions):
            card_position = instruction(card_position)

        if card_position in hit_positions:
            print('HIT')
            print(i)
            return

        hit_positions.add(card_position)

    print('Card:', card_position)

def read_instructions():
    with open('input.txt') as file:
        return [parse_instruction(l) for l in file]

def gen_cut_func(value: int):
    def cut(n: int):
        return (n + value) % DECK_SIZE
    return cut

def gen_deal_with_inc_func(value: int):
    val = pow(value, -1, DECK_SIZE)

    def deal_with_inc(n: int):
        return (n * val) % DECK_SIZE
    return deal_with_inc

def deal_new_stack(n: int):
    return DECK_SIZE - n - 1

def parse_instruction(line: str):
    if line.startswith('cut'):
        value = int(line.split(' ')[-1])
        return gen_cut_func(value)

    if line.startswith('deal with increment'):
        value = int(line.split(' ')[-1])
        return gen_deal_with_inc_func(value)

    if line.startswith('deal into new stack'):
        return deal_new_stack

    raise Exception('Invalid instruction')


if __name__ == '__main__':
    main()
