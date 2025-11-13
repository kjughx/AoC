#!/bin/env python3
import numpy as np


def dst(p1, p2):
    n = 0
    for r in range(p1[0], p2[0]):
        if all(grid[r, :] == '.'):
            n += 1_000_000  # part 2
        else:
            n += 1

    for c in range(p1[1], p2[1]):
        if all(grid[:, c] == '.'):
            n += 1_000_000  # part 2
        else:
            n += 1
    return n


grid = np.array([[c for c in line.strip()] for line in open(0).readlines()])

R = len(grid)
C = len(grid[0])

gl = np.where(grid == '#')
gl = [(i, j) for i, j in zip(gl[0], gl[1])]

dsts = [dst(g1, g2) for g1 in gl for g2 in gl if g1 != g2]
print(sum(dsts))
