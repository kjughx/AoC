#!/bin/env python3
from collections import deque, defaultdict
import numpy as np
from timer import profiler


@profiler
def part1(heads):
    tails = defaultdict(set)
    q = deque(heads)
    while q:
        r, c, sr, sc = q.popleft()
        if grid[r, c] == '9':
            tails[(sr, sc)].add((r, c))
            continue

        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r+dr, c+dc

            if 0 <= nr < R and 0 <= nc < C:
                if grid[nr, nc].isdigit() and int(grid[nr, nc]) == int(grid[r, c]) + 1:
                    q.append((nr, nc, sr, sc))

    p = 0
    for head, tail in tails.items():
        p += len(tail)

    print(p)


@profiler
def part2(heads):
    tails = defaultdict(list)
    q = deque(heads)
    while q:
        r, c, sr, sc = q.popleft()
        if grid[r, c] == '9':
            tails[(sr, sc)].append((r, c))
            continue

        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r+dr, c+dc

            if 0 <= nr < R and 0 <= nc < C:
                if grid[nr, nc].isdigit() and int(grid[nr, nc]) == int(grid[r, c]) + 1:
                    q.append((nr, nc, sr, sc))

    p = 0
    for head, tail in tails.items():
        p += len(tail)

    print(p)


with open(0) as file:
    grid = np.matrix([[c for c in line.strip()] for line in file.readlines()])
    R, C = np.shape(grid)

    heads = []

    for r, c in zip(np.where(grid == '0')[0], np.where(grid == '0')[1]):
        heads.append((r, c, r, c))

    part1(heads)
    part2(heads)
