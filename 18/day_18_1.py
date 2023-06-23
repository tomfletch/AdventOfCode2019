#!/usr/bin/env python3
from typing import List, NamedTuple, Set, Dict

class Vault(NamedTuple):
    plan: str
    width: int
    height: int
    all_keys: int

class Point(NamedTuple):
    x: int
    y: int

class GameState(NamedTuple):
    player: Point
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
        # print_vault(vault, game_state)

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

def print_vault(vault: Vault, game_state: GameState):
    output = ''

    for y in range(vault.height):
        for x in range(vault.width):
            if game_state.player.x == x and game_state.player.y == y:
                output += '@'
            else:
                output += vault.plan[y * vault.width + x]
        output += '\n'

    print(output)
    print('Have Keys: ', game_state.keys)
    print()

def generate_next_game_states(vault: Vault, game_state: GameState):
    next_game_states: List[GameState] = []

    for direction in DIRECTIONS:
        next_game_state = generate_next_game_state(vault, game_state, direction)

        if next_game_state:
            next_game_states.append(next_game_state)

    return next_game_states

def generate_next_game_state(vault: Vault, game_state: GameState, direction: Point):
    new_player = Point(game_state.player.x + direction.x, game_state.player.y + direction.y)

    if new_player.x < 0 or new_player.x >= vault.width: return None
    if new_player.y < 0 or new_player.y >= vault.height: return None

    cell_index = new_player.y * vault.width + new_player.x
    cell = vault.plan[cell_index]

    if cell == '#': return None

    if cell >= 'A' and cell <= 'Z' and ((1 << (ord(cell) - ord('A'))) & game_state.keys) == 0:
        return None

    new_keys = game_state.keys

    if cell >= 'a' and cell <= 'z':
        val = ord(cell) - ord('a')
        new_keys |= 1 << val

    return GameState(new_player, new_keys)


def replace_at_index(s: str, index: int, new_char: str):
    return s[:index] + new_char + s[index+1:]

def read_vault():
    with open('test_1.txt') as file:
        plan_list = [line.strip() for line in file]
        height = len(plan_list)
        width = len(plan_list[0])

        plan = ''.join(plan_list)

        player_index = plan.index('@')
        plan = replace_at_index(plan, player_index, '.')
        player = Point(player_index % width, player_index // width)

        all_keys = 0

        for y in range(height):
            for x in range(width):
                cell = plan_list[y][x]
                if cell >= 'a' and cell <= 'z':
                    val = ord(cell) - ord('a')
                    all_keys |= 1 << val

        return (Vault(plan, width, height, all_keys), GameState(player, 0))

if __name__ == '__main__':
    main()
