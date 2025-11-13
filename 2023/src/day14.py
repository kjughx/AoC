#!/bin/env python3
import numpy as np
from collections import deque

grid = np.array([[c for c in line.strip()] for line in open(0).readlines()])

R = grid.shape[0]
C = grid.shape[1]

def shift(grid, d):
    # split on '#' and shift the O's to the "beginning"
    for i in range(R):
        if d in 'ns':
            slz = grid[:, i]
        else:
            slz = grid[i, :]

        os = [sorted(o, reverse=(d in "nw")) for o in ''.join(slz).split('#')]
        slz = [c for c in "#".join([''.join(o) for o in os])]

        if d in 'ns':
            grid[:, i] = slz
        else:
            grid[i, :] = slz

    return grid

grid = shift(grid, 'n')
os = list(zip(np.where(grid == 'O')[0], np.where(grid == 'O')[1]))
t = 0
for r, _ in os:
    t += (R-r)
print(t)

seen = []
N = 0
while True:
    os = list(zip(np.where(grid == 'O')[0], np.where(grid == 'O')[1]))
    if os in seen:
        break
    N += 1

    seen.append(os)
    for d in ['n', 'w', 's', 'e']:
        grid = shift(grid, d)

os = list(zip(np.where(grid == 'O')[0], np.where(grid == 'O')[1]))
# So now we know it repeats, the final 'os' is then:
i = seen.index(os)
os = seen[i + (1000000000 - i) % (N - i)]

t = 0
for r, _ in os:
    t += (R-r)
print(t)
