#!/usr/bin/env python3
from typing import List

def main():
    module_masses = read_masses()
    total_fuel = sum(calculate_module_fuel(m) for m in module_masses)

    print(f'Total fuel: {total_fuel}')

def calculate_module_fuel(mass: int) -> int:
    module_fuel = mass//3 - 2

    fuel_for_fuel = 0
    extra_fuel = module_fuel//3 - 2

    while extra_fuel > 0:
        fuel_for_fuel += extra_fuel
        extra_fuel = extra_fuel//3 - 2

    return module_fuel + fuel_for_fuel

def read_masses() -> List[int]:
    with open('input.txt') as f:
        return [int(l) for l in f]

if __name__ == '__main__':
    main()
