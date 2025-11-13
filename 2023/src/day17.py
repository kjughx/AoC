#!/usr/bin/env python3
import numpy as np
from collections import deque
import math
from heapq import heapify, heappush, heappop

grid = np.array([list(map(int, [c for c in line.strip()])) for line in open(0).readlines()])
R = grid.shape[0]
C = grid.shape[1]

sr, sc = (0, 0)
er, ec = R - 1, C - 1

mhl = math.inf
steps = [(grid[sr + 1, sc], (sr + 1, sc, 1, 0, 1)), (grid[sr, sc + 1], (sr, sc + 1, 0, 1, 1))]

seen = set([(sr + 1, sc), (sr, sc + 1)])
while steps:
    hl, (r, c, dr, dc, n) = heappop(steps)

    if (r, c) == (er, ec):
        mhl = min(mhl, hl)
        break

    if (r, c, dr, dc, n) in seen:
        continue
    seen.add((r, c, dr, dc, n))

    if n < 3:
        nr, nc = r + dr, c + dc
        if 0 <= nr < R and 0 <= nc < C:
            heappush(steps, (hl + grid[nr, nc], (nr, nc, dr, dc, n + 1)))

    nr, nc = r + dc, c + dr
    if 0 <= nr < R and 0 <= nc < C:
        heappush(steps, (hl + grid[nr, nc], (nr, nc, dc, dr, 1)))
    nr, nc = r - dc, c - dr
    if 0 <= nr < R and 0 <= nc < C:
        heappush(steps, (hl + grid[nr, nc], (nr, nc, -dc, -dr, 1)))

print(mhl)

# # part 2

mhl = math.inf
# somehow the answer depends on the order of these....
steps = [(grid[sr + 1, sc], (sr + 1, sc, 1, 0, 1)), (grid[sr, sc + 1], (sr, sc + 1, 0, 1, 1))]
seen = set()
while steps:
    hl, (r, c, dr, dc, n) = heappop(steps)

    if (r, c) == (er, ec) and n >= 4:
        mhl = min(mhl, hl)
        break

    if (r, c, dr, dc, n) in seen:
        continue
    seen.add((r, c, dr, dc, n))

    if n < 10:
        nr, nc = r + dr, c + dc
        if 0 <= nr < R and 0 <= nc < C:
            heappush(steps, (hl + grid[nr, nc], (nr, nc, dr, dc, n + 1)))

    if n < 4:
        continue

    nr, nc = r + dc, c + dr
    if 0 <= nr < R and 0 <= nc < C:
        heappush(steps, (hl + grid[nr, nc], (nr, nc, dc, dr, 1)))

    nr, nc = r - dc, c - dr
    if 0 <= nr < R and 0 <= nc < C:
        heappush(steps, (hl + grid[nr, nc], (nr, nc, -dc, -dr, 1)))

print(mhl)
