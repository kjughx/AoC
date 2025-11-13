#!/bin/env python3
from collections import deque
import numpy as np
from timer import profiler

# pylsp: disable=E302,C0114,C0116,C0301,C0209,W1514,C0414,C0200,E0001

grid = np.array([[c for c in row.strip('\n')] for row in open(0).readlines()])
R, C = np.shape(grid)

walls = np.where(grid == '#')
walls = [(r, c) for r, c in zip(walls[0], walls[1])]

sr, sc = np.where(grid == 'S')
fr, fc = np.where(grid == 'E')

sr, sc = *sr, *sc
fr, fc = *fr, *fc

grid[sr, sc] = '.'
grid[fr, fc] = '.'

q = deque([(sr, sc, 0, [(sr, sc)])])

# First find without cheating
T = R * C
vis = {}
path = []
while q:
    r, c, t, p = q.popleft()
    if (r, c) == (fr, fc):
        T = min(T, t)
        path = p

    if (r, c) in vis and vis[(r, c)] < t:
        continue
    vis[(r, c)] = t

    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < R and 0 <= nc < C and grid[nr, nc] != '#':
            q.append((nr, nc, t + 1, p + [(nr, nc)]))


def reachable(r, c, t):
    vis = set()

    for d in range(t + 1):
        for dr in range(d + 1):
            dc = d - dr
            for nr, nc in {(r + dr, c + dc), (r - dr, c + dc), (r + dr, c - dc), (r - dr, c - dc)}:
                if (nr, nc) in path:
                    vis.add((nr, nc, d))
    return vis


@profiler
def solve(MC):
    p = 0
    TS = [0 for _ in range(T)]
    for r, c in path:
        p += 1
        for nr, nc, t in reachable(r, c, MC):
            t = len(path[:path.index((r, c))]) + t + \
                len(path[path.index((nr, nc)):]) - 1
            if t < T:
                TS[T - t] += 1
    print(np.sum(TS[100:]))


solve(2)
# solve(20)
