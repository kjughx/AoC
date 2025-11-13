#!/usr/bin/env python3
import numpy as np
from collections import deque

grid = np.array([[c for c in line.strip()] for line in open(0).readlines()])
R = grid.shape[0]
three = grid.shape[1]

start = tuple(map(int, (np.where(grid == 'S')[0][0], np.where(grid == 'S')[1][0])))

seen = {(*start, 0)}

q = deque()
for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
    r, c = start
    if grid[r + dr, c + dc] != '#':
        q.append((r + dr, c + dc, 1))
        seen.add((r + dr, c + dc, 1))

t = 0
while q:
    r, c, n = q.popleft()
    if n == 6:
        t += 1
        continue

    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = (r + dr), (c + dc)

        if (nr, nc, n + 1) not in seen and grid[nr % R, nc % three] != '#':
            q.append((nr, nc, n + 1))
            seen.add((nr, nc, n + 1))
print(t)

n = 26501365

xs = [65, 196, 327]
ys = [3877, 34674, 96159]

a = (ys[-1] - 2*ys[-2] + ys[-3]) / (xs[-1]**2 - 2*xs[-2]**2 + xs[-3]**2)
b = (ys[-1] - ys[-2] - a * xs[-1] ** 2 + a * xs[-2]**2) / (xs[-1] - xs[-2])
c = ys[-1] - a * xs[-1] ** 2 - b * xs[-1]

print(a * (n ** 2) + b * n + c)
