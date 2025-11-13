#!/bin/env python3

import numpy as np

with open('inputs/day22') as file:
    lines = [line.strip('\n') for line in file.readlines()]
    ipath = iter(lines[-1])

    c = next(ipath)
    path = []
    op = ''
    try:
        while True:
            if c == 'R' or c == 'L':
                path.append(op)
                path.append(c)
                c = next(ipath)
                op = ''
                continue

            op += c
            c = next(ipath)
    except:
        pass

    grid = lines[:-2]

    cr, cc = 0, grid[0].find('.')
    dr, dc = 0,1
    grid = [row + " " * (max([len(row) for row in grid]) - len(row)) for row in grid]
    lr, lc = len(grid), len(grid[0])

    for op in path:
        if op.isdigit():
            steps = int(op)
            for _ in range(steps):
                # step in direction, if it's not a '.' then wrap and keep trying
                nr, nc = cr, cc
                while True:
                    nr, nc = (nr + dr) % lr, (nc + dc) % lc
                    if grid[nr][nc] != ' ':
                        break
                if grid[nr][nc] == '#':
                    break
                cr, cc = nr, nc
        else:
            if op == 'R':
                dr, dc = dc, -dr
            else:
                dr, dc = -dc, dr

    cr, cc = cr+1, cc+1
    match (dr, dc):
        case [0, 1]: ans = 1000*cr + 4* cc + 0 
        case [1, 0]: ans = 1000*cr + 4* cc + 1
        case [0, -1]: ans = 1000*cr + 4* cc + 2 
        case [-1, 0]: ans = 1000*cr + 4* cc + 3 

    print("part1: ", ans)

    cr, cc = 0, grid[0].find('.')
    dr, dc = 0, 1

    import re
    for op in path:
        if op.isdigit():
            for _ in range(int(op)):
                cdr = dr
                cdc = dc
                nr = cr + dr
                nc = cc + dc
                if nr < 0 and 50 <= nc < 100 and dr == -1:
                    dr, dc = 0, 1
                    nr, nc = nc + 100, 0
                elif nc < 0 and 150 <= nr < 200 and dc == -1:
                    dr, dc = 1, 0
                    nr, nc = 0, nr - 100
                elif nr < 0 and 100 <= nc < 150 and dr == -1:
                    nr, nc = 199, nc - 100
                elif nr >= 200 and 0 <= nc < 50 and dr == 1:
                    nr, nc = 0, nc + 100
                elif nc >= 150 and 0 <= nr < 50 and dc == 1:
                    dc = -1
                    nr, nc = 149 - nr, 99
                elif nc == 100 and 100 <= nr < 150 and dc == 1:
                    dc = -1
                    nr, nc = 149 - nr, 149
                elif nr == 50 and 100 <= nc < 150 and dr == 1:
                    dr, dc = 0, -1
                    nr, nc = nc - 50, 99
                elif nc == 100 and 50 <= nr < 100 and dc == 1:
                    dr, dc = -1, 0
                    nr, nc = 49, nr + 50
                elif nr == 150 and 50 <= nc < 100 and dr == 1:
                    dr, dc = 0, -1
                    nr, nc = nc + 100, 49
                elif nc == 50 and 150 <= nr < 200 and dc == 1:
                    dr, dc = -1, 0
                    nr, nc = 149, nr - 100
                elif nr == 99 and 0 <= nc < 50 and dr == -1:
                    dr, dc = 0, 1
                    nr, nc = nc + 50, 50
                elif nc == 49 and 50 <= nr < 100 and dc == -1:
                    dr, dc = 1, 0
                    nr, nc = 100, nr - 50
                elif nc == 49 and 0 <= nr < 50 and dc == -1:
                    dc = 1
                    nr, nc = 149 - nr, 0
                elif nc < 0 and 100 <= nr < 150 and dc == -1:
                    dc = 1
                    nr, nc = 149 - nr, 50
                if grid[nr][nc] == "#":
                    dr = cdr
                    dc = cdc
                    break
                cr = nr
                cc = nc

        elif op == "R":
            dr, dc = dc, -dr
        elif op == "L":
            dr, dc = -dc, dr

    cr, cc = cr+1, cc+1
    match (dr, dc):
        case [0, 1]: ans = 1000*cr + 4* cc + 0 
        case [1, 0]: ans = 1000*cr + 4* cc + 1
        case [0, -1]: ans = 1000*cr + 4* cc + 2 
        case [-1, 0]: ans = 1000*cr + 4* cc + 3 

    print("part2: ", ans)
