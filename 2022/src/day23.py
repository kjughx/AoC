#!/bin/env python3 
from collections import deque
from typing import Tuple

with open('inputs/day23') as file:
    lines = [line.strip() for line in file.readlines()]
    positions = set()

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                positions.add((x, y))

    checks = {'N': [(-1,-1), (0,-1), (1, -1)],
              'S': [(-1, 1), (0, 1), (1,  1)],
              'W': [(-1, 1), (-1, 0), (-1, -1)],
              'E': [(1, 1), (1, 0), (1, -1)]}


    directions = deque(['N', 'S', 'W', 'E'])
    movements = {'N': (0, -1), 'S': (0, 1), 'W': (-1, 0), 'E': (1, 0)}

    neighbors = [(-1,-1), (0,-1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]

    i = 0
    while True:
        i += 1
        npositions = {}
        moved = False
        for x,y in positions:
            if not any((x + dx, y + dy) in positions for dx, dy in neighbors):
                continue
            valid = False
            proposed_directions = directions.copy()
            while not valid and proposed_directions:
                proposed_direction = proposed_directions.popleft()
                if not any((x+dx, y+dy) in positions for dx,dy in checks[proposed_direction]):
                    dx,dy = movements[proposed_direction]
                    if (x + dx, y + dy) in npositions:
                        npositions[(x + dx, y + dy)] = 0
                    else:
                        npositions[(x + dx, y + dy)] = (x, y)
                        valid = True
                    break
            
        for npos, opos in npositions.items():
            if isinstance(opos, Tuple):
                moved = True
                positions.remove(opos)
                positions.add(npos)
        if not moved:
            print("Part 2: ", i)
            break
        directions.rotate(-1)
    
    minx, maxx = min([x for x,_ in positions]), max([x for x,_ in positions])
    miny, maxy = min([y for _,y in positions]), max([y for _,y in positions])
    print("Part 1: ", (1 + maxx-minx) * (1 + maxy-miny) - len(positions))
