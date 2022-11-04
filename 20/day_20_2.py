#!/usr/bin/env python3
from collections import defaultdict
from typing import NamedTuple, Set, DefaultDict, List, Dict

class Point(NamedTuple):
    x: int
    y: int

class Player(NamedTuple):
    pos: Point
    level: int

class Donut(NamedTuple):
    passages: Set[Point]
    portals: Dict[Point, Point]
    start: Point
    end: Point
    max_x: int
    max_y: int

def main():
    donut = read_donut()

    startPlayer = Player(donut.start, 0)

    seen: Set[Player] = set()
    next_points = [startPlayer]
    dist = {startPlayer: 0}

    while next_points:
        current_player = next_points.pop(0)

        if current_player.level == 0 and current_player.pos == donut.end:
            print('Steps:', dist[current_player])
            break

        neighbours = get_neighbours(donut, current_player)

        for neighbour in neighbours:
            if neighbour not in seen:
                next_points.append(neighbour)
                dist[neighbour] = dist[current_player] + 1
                seen.add(neighbour)

DIRECTIONS = [
    Point(-1, 0),
    Point(1, 0),
    Point(0, -1),
    Point(0, 1)
]

def is_outer_portal(donut: Donut, pos: Point):
    if pos.x == 2: return True
    if pos.y == 2: return True
    if pos.x == donut.max_x: return True
    if pos.y == donut.max_y: return True

    return False


def get_neighbours(donut: Donut, current_player: Player):
    neighbours: List[Player] = []
    current_point = current_player.pos

    for direction in DIRECTIONS:
        next_point = Point(current_point.x + direction.x, current_point.y + direction.y)

        if next_point in donut.passages:
            neighbours.append(Player(next_point, current_player.level))
        elif current_point in donut.portals:

            if is_outer_portal(donut, current_point):
                next_level = current_player.level - 1
            else:
                next_level = current_player.level + 1

            if next_level >= 0:
                neighbours.append(Player(donut.portals[current_point], next_level))

    return neighbours

def read_donut():

    with open('input.txt') as file:
        plan: List[List[str]] = [list(l) for l in file]

    passages: Set[Point] = set()

    for y, row in enumerate(plan):
        for x, cell in enumerate(row):
            if cell == '.':
                passages.add(Point(x, y))

    portal_ids: DefaultDict[str, List[Point]] = defaultdict(list)

    plan_height = len(plan)
    plan_width = max(len(row) for row in plan)

    # Find horizontal portals
    for y in range(plan_height):
        for x in range(plan_width - 2):
            part = plan[y][x] + plan[y][x+1] + plan[y][x+2]

            if part[0] == '.' and part[1:3].isalpha():
                portal_id = part[1:3]
                portal_ids[portal_id].append(Point(x, y))

            if part[0:2].isalpha() and part[2] == '.':
                portal_id = part[0:2]
                portal_ids[portal_id].append(Point(x+2, y))

    # Find vertical portals
    for y in range(plan_height - 2):
        for x in range(plan_width):
            part = plan[y][x] + plan[y+1][x] + plan[y+2][x]

            if part[0] == '.' and part[1:3].isalpha():
                portal_id = part[1:3]
                portal_ids[portal_id].append(Point(x, y))

            if part[0:2].isalpha() and part[2] == '.':
                portal_id = part[0:2]
                portal_ids[portal_id].append(Point(x, y+2))

    start = portal_ids['AA'][0]
    end = portal_ids['ZZ'][0]

    portals: Dict[Point, Point] = {}

    for this_portals in portal_ids.values():
        if len(this_portals) != 2: continue

        portals[this_portals[0]] = this_portals[1]
        portals[this_portals[1]] = this_portals[0]

    max_x = max(p.x for p in passages)
    max_y = max(p.y for p in passages)

    return Donut(passages, portals, start, end, max_x, max_y)



if __name__ == '__main__':
    main()
