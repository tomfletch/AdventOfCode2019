#!/usr/bin/env python3
from typing import List, NamedTuple, Set, Dict, Tuple

class Point(NamedTuple):
    x: int
    y: int

class Vault(NamedTuple):
    plan: str
    width: int
    height: int
    robots: Tuple[Point, Point, Point, Point]
    remaining_keys: int

DIRECTIONS = [
    Point(-1, 0),
    Point(1, 0),
    Point(0, -1),
    Point(0, 1)
]

def main():
    vault = read_vault()

    next_vaults = [vault]

    discovered: Set[Vault] = {vault}
    dist: Dict[Vault, int] = {vault: 0}

    success_vault = None

    while next_vaults:
        vault = next_vaults.pop(0)
        # print_vault(vault)

        if vault.remaining_keys == 0:
            success_vault = vault
            break

        new_vaults = generate_next_vaults(vault)

        for new_vault in new_vaults:
            if new_vault not in discovered:
                next_vaults.append(new_vault)
                discovered.add(new_vault)
                dist[new_vault] = dist[vault] + 1

    if success_vault:
        print('Steps:', dist[success_vault])


def print_vault(vault: Vault):
    output = ''

    for y in range(vault.height):
        for x in range(vault.width):
            output += get_cell(vault, x, y)
        output += '\n'

    print(output)

def get_cell(vault: Vault, x: int, y: int):
    for robot in vault.robots:
        if robot.x == x and robot.y == y:
            return '@'
    else:
        return vault.plan[y * vault.width + x]

def generate_next_vaults(vault: Vault):
    next_vaults: List[Vault] = []

    for robot_index in range(4):
        for direction in DIRECTIONS:
            next_vault = generate_next_vault(vault, robot_index, direction)

            if next_vault:
                next_vaults.append(next_vault)

    return next_vaults

def generate_next_vault(vault: Vault, robot_index: int, direction: Point):
    robot = vault.robots[robot_index]
    new_robot = Point(robot.x + direction.x, robot.y + direction.y)

    if new_robot.x < 0 or new_robot.x >= vault.width: return None
    if new_robot.y < 0 or new_robot.y >= vault.height: return None

    cell_index = new_robot.y * vault.width + new_robot.x
    cell = vault.plan[cell_index]

    if cell == '#' or (cell >= 'A' and cell <= 'Z'):
        return None

    new_remaining_keys = vault.remaining_keys

    new_plan = vault.plan

    if cell >= 'a' and cell <= 'z':
        new_remaining_keys -= 1
        new_plan = replace_at_index(new_plan, cell_index, '.')

        door_index = new_plan.find(cell.upper())
        if door_index != -1:
            new_plan = replace_at_index(new_plan, door_index, '.')

    new_robots = list(vault.robots)
    new_robots[robot_index] = new_robot

    return Vault(new_plan, vault.width, vault.height, tuple(new_robots), new_remaining_keys)


def replace_at_index(s: str, index: int, new_char: str):
    return s[:index] + new_char + s[index+1:]

def read_vault():
    with open('input.txt') as file:
        plan_list = [line.strip() for line in file]
        height = len(plan_list)
        width = len(plan_list[0])

        plan = ''.join(plan_list)

        player_index = plan.index('@')
        plan = replace_at_index(plan, player_index, '#')
        player = Point(player_index % width, player_index // width)

        plan = replace_at_index(plan, player.y * width + player.x - 1, '#')
        plan = replace_at_index(plan, player.y * width + player.x + 1, '#')
        plan = replace_at_index(plan, (player.y - 1) * width + player.x, '#')
        plan = replace_at_index(plan, (player.y + 1) * width + player.x, '#')

        robot_1 = Point(player.x - 1, player.y - 1)
        robot_2 = Point(player.x + 1, player.y - 1)
        robot_3 = Point(player.x - 1, player.y + 1)
        robot_4 = Point(player.x + 1, player.y + 1)

        remaining_keys = 0

        for i in plan:
            if i >= 'a' and i <= 'z':
                remaining_keys += 1

        return Vault(plan, width, height, (robot_1, robot_2, robot_3, robot_4), remaining_keys)

if __name__ == '__main__':
    main()
