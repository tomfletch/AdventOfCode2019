#!/usr/bin/env python3
from typing import List, Tuple, NamedTuple, Set, Dict, Union
import heapq

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

    key_positions = find_key_positions(vault)
    seen: Set[GameState] = set()
    next_states: List[Tuple[int, GameState]] = [(0, game_state)]
    dist = {game_state: 0}


    shortest_paths: Dict[Tuple[Point, Point], Dict[int, Union[int, None]]] = {}

    while next_states:
        _, current_state = heapq.heappop(next_states)
        # print(next_states)
        # print(current_state, dist[current_state])

        if current_state in seen:
            continue

        seen.add(current_state)

        if current_state.keys == vault.all_keys:
            print('Shortest Path:', dist[current_state])
            break

        new_next_states = get_next_states(vault, key_positions, current_state, shortest_paths)

        for next_state, next_state_cost in new_next_states:
            if next_state in seen:
                continue

            new_cost = dist[current_state] + next_state_cost

            if next_state not in dist or new_cost < dist[next_state]:
                dist[next_state] = new_cost
                heapq.heappush(next_states, (new_cost, next_state))



def get_next_states(vault: Vault, key_positions: Dict[str, Point], current_state: GameState, shortest_paths: Dict[Tuple[Point, Point], Dict[int, Union[int, None]]]):
    next_states: List[Tuple[GameState, int]] = []

    for key, key_pos in key_positions.items():
        new_key_bit = 1 << ord(key) - ord('a')
        if new_key_bit & current_state.keys != 0:
            continue

        shortest_path_length = get_shortest_path(vault, current_state.player, key_pos, current_state.keys, shortest_paths)

        if shortest_path_length is not None:
            next_states.append((GameState(key_pos, current_state.keys | new_key_bit), shortest_path_length))

    return next_states


def find_key_positions(vault: Vault):
    key_positions: Dict[str, Point] = {}

    for current_key in range(ord('a'), ord('z') + 1):
        key_index = vault.plan.find(chr(current_key))
        if key_index == -1: break

        key_positions[chr(current_key)] = Point(key_index % vault.width, key_index // vault.width)

    return key_positions

def is_valid_move(vault: Vault, new_player: Point, with_keys: int):

    if new_player.x < 0 or new_player.x >= vault.width: return False
    if new_player.y < 0 or new_player.y >= vault.height: return False

    cell_index = new_player.y * vault.width + new_player.x
    cell = vault.plan[cell_index]

    if cell == '#': return False

    if cell >= 'A' and cell <= 'Z' and ((1 << (ord(cell) - ord('A'))) & with_keys) == 0:
        return False

    return True

def generate_next_positions(vault: Vault, player: Point, with_keys: int):
    next_positions: List[Point] = []

    for direction in DIRECTIONS:
        new_player = Point(player.x + direction.x, player.y + direction.y)

        if is_valid_move(vault, new_player, with_keys):
            next_positions.append(new_player)

    return next_positions

def get_shortest_path(vault: Vault, from_pos: Point, to_pos: Point, with_keys: int, shortest_paths: Dict[Tuple[Point, Point], Dict[int, Union[int, None]]]):
    if (from_pos, to_pos) in shortest_paths:
        shortest_path_options = shortest_paths[(from_pos, to_pos)]

        if with_keys in shortest_path_options:
            return shortest_path_options[with_keys]

        for keys, cost in shortest_path_options.items():
            if with_keys & keys == keys and cost is not None:
                return cost

    shortest_path = find_shortest_path(vault, from_pos, to_pos, with_keys)

    if (from_pos, to_pos) not in shortest_paths:
        shortest_paths[(from_pos, to_pos)] = {}

    if not shortest_path:
        shortest_paths[(from_pos, to_pos)][with_keys] = None
        return None

    shortest_path_cost, required_keys = shortest_path



    shortest_paths[(from_pos, to_pos)][required_keys] = shortest_path_cost

    return shortest_path_cost


def find_shortest_path(vault: Vault, from_pos: Point, to_pos: Point, with_keys: int):
    next_positions: List[Tuple[Point, int]] = [(from_pos, 0)]

    dist: Dict[Point, int] = {}
    dist[from_pos] = 0

    visited: Set[Point] = {from_pos}

    while next_positions:
        current_pos, required_keys = next_positions.pop(0)
        # print(current_pos)

        if current_pos == to_pos:
            return (dist[current_pos], required_keys)

        new_positions = generate_next_positions(vault, current_pos, with_keys)

        for new_position in new_positions:
            this_required_keys = required_keys

            new_cell = vault.plan[new_position.y * vault.width + new_position.x]

            if new_cell >= 'A' and new_cell <= 'Z':
                this_required_keys |= 1 << (ord(new_cell) - ord('A'))

            if new_position not in visited:
                visited.add(new_position)
                dist[new_position] = dist[current_pos] + 1
                next_positions.append((new_position, this_required_keys))



def replace_at_index(s: str, index: int, new_char: str):
    return s[:index] + new_char + s[index+1:]

def read_vault():
    with open('input.txt') as file:
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
