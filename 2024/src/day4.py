#!/bin/env python3
from timer import profiler
import numpy as np


def slice(a, r, dr, c, dc, s):
    try:
        ret = []
        for t in range(s):
            if r + dr * t < 0:
                raise IndexError
            if c + dc * t < 0:
                raise IndexError

            ret.append(a[r + dr*t, c + dc*t])
        return ret
    except IndexError:
        return []


@profiler
def part1(grid):
    p = 0
    R, C = np.shape(grid)

    xs = np.where(grid == 'X')
    for r, c in zip(xs[0], xs[1]):
        for (dr, dc) in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            if slice(grid, r, dr, c, dc, 4) == ['X', 'M', 'A', 'S']:
                p += 1
    print(p)


@profiler
def part2(grid):
    p = 0
    R, C = np.shape(grid)
    xs = np.where(grid == 'A')
    for r, c in zip(xs[0], xs[1]):
        count = 0
        for (dr, dc) in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            if slice(grid, r - dr, dr, c - dc, dc, 3) == ['M', 'A', 'S']:
                count += 1
        if count == 2:
            p += 1
    print(p)


with open(0) as file:
    grid = np.array([[a for a in line.strip()] for line in file.readlines()])

    part1(grid)
    part2(grid)
