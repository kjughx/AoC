#!/bin/env python3

import numpy as np
from collections import deque

lines = np.array([[c for c in line.strip()] for line in open(0).readlines()])
R = lines.shape[0]
C = lines.shape[1]

def f(sr, sc, dr, dc):
    energized = np.array([[0 for _ in range(lines.shape[1])] for _ in range(lines.shape[0])])

    rays = deque([((sr, sc), (dr, dc))])

    seen = set()
    while rays:
        (r, c), (dr, dc) = rays.popleft()
        if ((r, c), (dr, dc)) in seen:
            continue
        nr, nc = r + dr, c + dc

        if 0 <= nr < R and 0 <= nc < C:
            if lines[nr, nc] == '.':
                rays.append(((nr, nc), (dr, dc)))
            elif lines[nr, nc] == '-':
                if (dr, dc) in [(0, 1), (0, -1)]:
                    rays.append(((nr, nc), (dr, dc)))
                else:
                    rays.append(((nr, nc), (0, 1)))
                    rays.append(((nr, nc), (0, -1)))
            elif lines[nr, nc] == '|':
                if (dr, dc) in [(1, 0), (-1, 0)]:
                    rays.append(((nr, nc), (dr, dc)))
                else:
                    rays.append(((nr, nc), (1, 0)))
                    rays.append(((nr, nc), (-1, 0)))
            elif lines[nr, nc] == '\\':
                rays.append(((nr, nc), (dc, dr)))
            elif lines[nr, nc] == '/':
                rays.append(((nr, nc), (-dc, -dr)))

            energized[nr, nc] = 1
            seen.add(((r, c), (dr, dc)))

    return sum(sum(energized))

# corners
m = max(f(0, -1, 0, 1),\
        f(-1, 0, 1, 0),\
        f(0, C, 0, -1),\
        f(0, C - 1, 1, 0),\
        f(R, 0, -1, 0),\
        f(R - 1, -1, 0, 1),\
        f(R, C - 1, -1, 0),\
        f(R - 1, C, 0, -1))

for r in range(1, R):
    m = max(m, f(r, C, 0, -1), f(r, -1, 0, 1))
for c in range(1, C):
    m = max(m, f(-1, c, 1, 0), f(R, c, -1, 0))
print(m)

