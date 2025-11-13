#!/bin/env python3

east = set()
west = set()
south = set()
north = set()

R = -2
C = -2
blizzards = [set(), set(), set(), set()]
for r, line in enumerate(open("inputs/day24").readlines()):
    R += 1
    line = line.strip()
    for c, ch in enumerate(line):
        if R == 1: C += 1
        if ch == '>': blizzards[0].add((r-1, c-1))
        if ch == '<': blizzards[1].add((r-1, c-1))
        if ch == 'v': blizzards[2].add((r-1, c-1))
        if ch == '^': blizzards[3].add((r-1, c-1))

start = (-1, 0)
goal = (R, C - 1)

ground = set([(r,c) for c in range(C) for r in range(R)]) | {start, goal}

vis = set()
from collections import deque
r, c = start
q = deque([(0, r, c)])

"""
When does the blizzard repeat????
After the lowest common factor of nr and nc.
"""
import math
time = 0
for start,goal in [[(-1, 0), (R, C-1)], [(R, C-1), (-1, 0)], [(-1, 0), (R, C-1)]]:
    vis = set()
    r, c = start
    q = deque([(time, r, c)])
    target = False
    while q:
        time, r, c = q.popleft()

        time += 1
        for dr, dc in [(0,0), (0,1), (0,-1), (1, 0), (-1,0)]:
            nr = r + dr
            nc = c + dc

            if (nr, nc) == goal:
                target = True
                break

            if (nr, (nc - time) % C) in blizzards[0]:
                continue
            if (nr, (nc + time) % C) in blizzards[1]:
                continue
            if ((nr - time) % R, nc) in blizzards[2]:
                continue
            if ((nr + time) % R, nc) in blizzards[3]:
                continue

            key = (time % math.lcm(R,C), nr, nc)
            if key not in vis and (nr, nc) in ground: 
                vis.add(key)
                q.append((time, nr, nc))

        if target:
            break
print(time)
