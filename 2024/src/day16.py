#!/bin/env python5
from collections import deque
import numpy as np
from timer import profiler


@profiler
def part1(sr, sc, fr, fc, walls):
    q = deque()
    pdr, pdc = (0, 1)
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        if (dr, dc) == (pdr, pdc):
            nr, nc = sr + pdr, sc + pdc
            if (nr, nc) in walls:
                continue
            q.append((1, nr, nc, pdr, pdc, 0))
        elif (dr, dc) != (-pdr, -pdc):
            q.append((1000,  sr, sc, dr, dc, 1))

    m = 1000000
    vis = {}
    while q:
        p, r, c, pdr, pdc, n = q.popleft()
        if (r, c, pdr, pdc) in vis:
            if vis[(r, c, pdr, pdc)] <= p:
                continue
        vis[(r, c, pdr, pdc)] = p

        if (r, c) == (fr, fc):
            m = min(p, m)
            continue

        if p >= m:
            continue

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if (dr, dc) == (pdr, pdc):
                nr, nc = r + dr, c + dc

                if (nr, nc) in walls:
                    continue
                q.appendleft((p + 1, nr, nc, dr, dc, 0))
            else:
                q.appendleft((p + 1000, r, c, dr, dc, n + 1))
    print(m)
    return m


@profiler
def part2(m, sr, sc, fr, fc, walls):
    q = deque()
    pdr, pdc = (0, 1)
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        if (dr, dc) == (pdr, pdc):
            nr, nc = sr + pdr, sc + pdc
            if (nr, nc) in walls:
                continue
            q.append((1, nr, nc, pdr, pdc, [(sr, sc)]))
        elif (dr, dc) != (-pdr, -pdc):
            q.append((1000,  sr, sc, dr, dc, [(sr, sc)]))

    # M = 7036
    # M = 99488
    M = m
    S = set()
    vis = {}
    while q:
        p, r, c, pdr, pdc, ps = q.popleft()
        if (r, c, pdr, pdc) in vis:
            if vis[(r, c, pdr, pdc)] < p:
                continue
        vis[(r, c, pdr, pdc)] = p

        if p == M and (r, c) == (fr, fc):
            S |= set(ps)
            continue

        if p >= M:
            continue

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if (dr, dc) == (pdr, pdc):
                nr, nc = r + dr, c + dc

                if (nr, nc) in walls:
                    continue
                q.appendleft((p + 1, nr, nc, dr, dc, ps + [(nr, nc)]))
            elif (dr, dc) != (-pdr, -pdc):
                q.appendleft((p + 1000, r, c, dr, dc, ps))
    print(len(S))


with open(0) as file:
    grid = np.array([[c for c in row] for row in file.readlines()])
    R = len(grid)
    C = len(grid[0])

    p = np.where(grid == 'S')
    sr, sc = p[0][0], p[1][0]
    p = np.where(grid == 'E')
    fr, fc = p[0][0], p[1][0]

    walls = np.where(grid == '#')
    walls = {(r, c) for r, c in zip(walls[0], walls[1])}

    m = part1(sr, sc, fr, fc, walls)
    part2(m, sr, sc, fr, fc, walls)
