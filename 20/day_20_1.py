#!/usr/bin/env python3
from collections import defaultdict
from typing import NamedTuple, Set, DefaultDict, List, Dict

class Point(NamedTuple):
    x: int
    y: int

class Donut(NamedTuple):
    passages: Set[Point]
    portals: Dict[Point, Point]
    start: Point
    end: Point

def main():
    donut = read_donut()

    seen: Set[Point] = set()
    next_points = [donut.start]
    dist = {donut.start: 0}

    while next_points:
        current_point = next_points.pop(0)

        if current_point == donut.end:
            print('Steps:', dist[current_point])
            break

        neighbours = get_neighbours(donut, current_point)

        for neighbour in neighbours:
            if neighbour not in seen:
                next_points.append(neighbour)
                dist[neighbour] = dist[current_point] + 1
                seen.add(neighbour)

DIRECTIONS = [
    Point(-1, 0),
    Point(1, 0),
    Point(0, -1),
    Point(0, 1)
]

def get_neighbours(donut: Donut, current_point: Point):
    neighbours: List[Point] = []

    for direction in DIRECTIONS:
        next_point = Point(current_point.x + direction.x, current_point.y + direction.y)

        if next_point in donut.passages:
            neighbours.append(next_point)
        elif current_point in donut.portals:
            neighbours.append(donut.portals[current_point])

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

    return Donut(passages, portals, start, end)



if __name__ == '__main__':
    main()
