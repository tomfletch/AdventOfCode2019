#!/usr/bin/env python3
from typing import List, NamedTuple, Set, Dict, Tuple

class Vault(NamedTuple):
    plan: str
    width: int
    height: int
    all_keys: int

class Point(NamedTuple):
    x: int
    y: int

class GameState(NamedTuple):
    robots: Tuple[Point, Point, Point, Point]
    keys: int

DIRECTIONS = [
    Point(-1, 0),
    Point(1, 0),
    Point(0, -1),
    Point(0, 1)
]

def main():
    vault, game_state = read_vault()

    next_game_states = [game_state]

    discovered: Set[GameState] = {game_state}
    dist: Dict[GameState, int] = {game_state: 0}

    success_state = None

    while next_game_states:
        game_state = next_game_states.pop(0)

        if vault.all_keys == game_state.keys:
            success_state = game_state
            break

        new_game_states = generate_next_game_states(vault, game_state)

        for new_game_state in new_game_states:
            if new_game_state not in discovered:
                next_game_states.append(new_game_state)
                discovered.add(new_game_state)
                dist[new_game_state] = dist[game_state] + 1

    if success_state:
        print('Steps:', dist[success_state])


def generate_next_game_states(vault: Vault, game_state: GameState):
    next_game_states: List[GameState] = []

    for robot_index in range(4):
        for direction in DIRECTIONS:
            next_game_state = generate_next_game_state(vault, game_state, robot_index, direction)

            if next_game_state:
                next_game_states.append(next_game_state)

    return next_game_states

def generate_next_game_state(vault: Vault, game_state: GameState, robot_index: int, direction: Point):
    new_robot = Point(game_state.robots[robot_index].x + direction.x, game_state.robots[robot_index].y + direction.y)

    if new_robot.x < 0 or new_robot.x >= vault.width: return None
    if new_robot.y < 0 or new_robot.y >= vault.height: return None

    cell_index = new_robot.y * vault.width + new_robot.x
    cell = vault.plan[cell_index]

    if cell == '#': return None

    if cell >= 'A' and cell <= 'Z' and ((1 << (ord(cell) - ord('A'))) & game_state.keys) == 0:
        return None

    new_keys = game_state.keys

    if cell >= 'a' and cell <= 'z':
        val = ord(cell) - ord('a')
        new_keys |= 1 << val

    new_robots = list(game_state.robots)
    new_robots[robot_index] = new_robot

    return GameState(tuple(new_robots), new_keys)


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

        all_keys = 0

        for y in range(height):
            for x in range(width):
                cell = plan_list[y][x]
                if cell >= 'a' and cell <= 'z':
                    val = ord(cell) - ord('a')
                    all_keys |= 1 << val

        return (Vault(plan, width, height, all_keys), GameState((robot_1, robot_2, robot_3, robot_4), 0))

if __name__ == '__main__':
    main()
