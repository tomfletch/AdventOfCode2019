#!/usr/bin/env python3

def main():
    module_masses = read_masses()
    module_fuel = [m//3 - 2 for m in module_masses]
    total_fuel = sum(module_fuel)
    print(f'Total fuel: {total_fuel}')

def read_masses():
    with open('input.txt') as f:
        return [int(l) for l in f]

if __name__ == '__main__':
    main()
