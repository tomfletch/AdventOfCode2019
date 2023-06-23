#!/usr/bin/env python3.11
DECK_SIZE = 10007
CARD = 2019

def main():
    instructions = read_instructions()
    card_position = CARD

    for instruction in instructions:
        card_position = instruction(card_position)

    print('Card position:', card_position)


def read_instructions():
    with open('input.txt') as file:
        return [parse_instruction(l) for l in file]

def gen_cut_func(value: int):
    def cut(n: int):
        return (n + value) % DECK_SIZE
    return cut

def gen_deal_with_inc_func(value: int):
    def deal_with_inc(n: int):
        return n * value % DECK_SIZE
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
