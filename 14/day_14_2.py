#!/usr/bin/env python3
from typing import Dict, List, NamedTuple
from collections import defaultdict
import math

MAX_ORE = 1000000000000

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

        if not self.chemicals[reaction.output.chemical]:
            del self.chemicals[reaction.output.chemical]

        for input in reaction.inputs:
            self.chemicals[input.chemical] += input.quantity * reaction_times

            if not self.chemicals[input.chemical]:
                del self.chemicals[input.chemical]

    def reverse_reactions(self, reactions: List[Reaction]) -> bool:
        was_any_performed = False
        while True:
            reaction_performed = False

            for reaction in reactions:
                this_reaction_performed = self.reverse_reaction(reaction)

                if this_reaction_performed:
                    reaction_performed = True
                    was_any_performed = True

            if not reaction_performed:
                break

        return was_any_performed

    def reverse_reaction(self, reaction: Reaction):
        reverse_time = self.chemicals[reaction.output.chemical] // -reaction.output.quantity

        if reverse_time <= 0:
            return False

        self.chemicals[reaction.output.chemical] += reaction.output.quantity * reverse_time

        for input in reaction.inputs:
            self.chemicals[input.chemical] -= input.quantity * reverse_time

        return True

    def is_all_ore(self) -> bool:
        chemicals = list(self.chemicals.items())
        chemicals = [c for c in chemicals if c[0] != 'ORE']
        chemicals = [c for c in chemicals if c[1] > 0]
        return len(chemicals) == 0

    def count_ore(self) -> int:
        return self.chemicals['ORE']

    def multiply_inventory(self, mult: int):
        for chemical in self.chemicals.keys():
            self.chemicals[chemical] *= mult

def main():
    reactions = read_reactions()
    inventory = Inventory()

    while not inventory.is_all_ore():
        chemical = inventory.get_next_chemical()
        reaction = reactions[chemical]
        inventory.perform_reaction(reaction)

    ore_count = inventory.count_ore()
    fuel_count = MAX_ORE // ore_count
    single_fuel_chemicals = inventory.chemicals.copy()
    inventory.multiply_inventory(fuel_count)
    ore_count = inventory.count_ore()


    inventory.reverse_reactions(list(reactions.values()))

    while True:
        inventory.reverse_reactions(list(reactions.values()))
        ore_count = inventory.count_ore()
        print('ore', ore_count)

        ore_remaining = MAX_ORE - ore_count
        print('remaining', ore_remaining)
        print('single', single_fuel_chemicals['ORE'])
        mult = ore_remaining // single_fuel_chemicals['ORE']
        print('mult', mult)

        if mult < 1:
            break

        fuel_count += mult

        for chemical, quantity in single_fuel_chemicals.items():
            inventory.chemicals[chemical] += quantity * mult

    ore_count = inventory.count_ore()

    while ore_count < MAX_ORE:
        inventory.chemicals['FUEL'] += 1
        fuel_count += 1

        while not inventory.is_all_ore():
            chemical = inventory.get_next_chemical()
            reaction = reactions[chemical]
            inventory.perform_reaction(reaction)

        ore_count = inventory.count_ore()

    fuel_count -= 1

    print('Max fuel:', fuel_count)



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
