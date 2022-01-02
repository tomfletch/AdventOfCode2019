#!/usr/bin/env python3
from typing import Dict, List, NamedTuple
from collections import defaultdict
import math

class ChemicalQuantity(NamedTuple):
    chemical: str
    quantity: int

class Reaction(NamedTuple):
    inputs: List[ChemicalQuantity]
    output: ChemicalQuantity

class Inventory:
    def __init__(self):
        self.chemicals: Dict[str, int] = defaultdict(int)
        self.chemicals['FUEL'] = 1

    def get_next_chemical(self) -> str:
        chemicals = list(self.chemicals.items())
        chemicals = [c for c in chemicals if c[0] != 'ORE']
        chemicals = [c for c in chemicals if c[1] > 0]
        return chemicals[0][0]

    def perform_reaction(self, reaction: Reaction):
        inventory_quantity = self.chemicals[reaction.output.chemical]
        reaction_output_quantity = reaction.output.quantity
        reaction_times = math.ceil(inventory_quantity / reaction_output_quantity)

        self.chemicals[reaction.output.chemical] -= reaction_output_quantity * reaction_times

        for input in reaction.inputs:
            self.chemicals[input.chemical] += input.quantity * reaction_times

    def is_all_ore(self) -> bool:
        chemicals = list(self.chemicals.items())
        chemicals = [c for c in chemicals if c[0] != 'ORE']
        chemicals = [c for c in chemicals if c[1] > 0]
        return len(chemicals) == 0

    def count_ore(self) -> int:
        return self.chemicals['ORE']

def main():
    reactions = read_reactions()
    inventory = Inventory()

    while not inventory.is_all_ore():
        chemical = inventory.get_next_chemical()
        reaction = reactions[chemical]
        inventory.perform_reaction(reaction)

    print('Ore required:', inventory.count_ore())


def read_reactions() -> Dict[str, Reaction]:
    reactions: Dict[str, Reaction] = {}

    with open('input.txt') as f:
        for line in f:
            reaction = parse_reaction(line)
            reactions[reaction.output.chemical] = reaction

    return reactions

def parse_reaction(reaction_str: str) -> Reaction:
    # Example: 7 A, 1 D => 1 E
    inputs_str, output_str = reaction_str.strip().split(' => ')
    inputs = [parse_chemical_quantity(input_str) for input_str in inputs_str.split(',')]
    output = parse_chemical_quantity(output_str)
    return Reaction(inputs, output)

def parse_chemical_quantity(chemical_quantity_str: str) -> ChemicalQuantity:
    quantity, chemical = chemical_quantity_str.strip().split(' ')
    return ChemicalQuantity(chemical, int(quantity))


if __name__ == '__main__':
    main()
