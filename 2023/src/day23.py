#!/usr/bin/env python3
import numpy as np
from collections import deque
import sys

grid = np.array([[c for c in line.strip()] for line in open(0).readlines()])
R = grid.shape[0]
C = grid.shape[1]

sr, sc = 0, np.where(grid[0, :] == '.')[0][0]
er, ec = grid.shape[0] - 1, np.where(grid[grid.shape[0] - 1, :] == '.')[0][0]
ds = {'>': (0, 1), '<': (0, -1), 'v': (1, 0), '^': (-1, 0)}

sys.setrecursionlimit(10000000)

# part 1
steps = deque([((sr + 1, sc), {(sr + 1, sc): 1, (sr, sc): 0})])
ml = 0
while steps:
    (r, c), seen = steps.popleft()
    if (r, c) == (er, ec):
        ml = max(len(seen) - 1, ml)
        continue

    if grid[r, c] in '><v^':
        dr, dc = ds[grid[r, c]]
        if (r + dr, c + dc) not in seen:
            steps.append(((r + dr, c + dc), seen | {(r + dr, c + dc): seen[(r, c)] + 1}))
        continue

    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        if grid[r + dr, c + dc] != '#':
            if (r + dr, c + dc) not in seen:
                steps.append(((r + dr, c + dc), seen | {(r + dr, c + dc): seen[(r,c)] + 1}))
print(ml)

# part 2

"""
need to keep track of the junctions, where the path splits.
Then i need to find the distance between all junctions.
"""

junctions = set([(sr, sc), (er, ec)])

for r in range(R):
    for c in range(C):
        nbrs = sum([1 if (0 <= r + dr < R and 0 <= c + dc < C) and grid[r + dr, c + dc] != '#' else 0 for (dr, dc) in [(0, 1), (0, -1), (1, 0), (-1, 0)]])
        if nbrs > 2: # then it's a junction
            if grid[r, c] != '#':
                junctions.add((r,c))

distances = {}

for jr, jc in junctions:
    steps = deque([(jr, jc, 0)])
    distances[(jr, jc)] = {}
    seen = set()
    while steps:
        r, c, d = steps.popleft()
        if (r, c) in seen:
            continue
        seen.add((r, c))

        if (r, c) in junctions and (r, c) != (jr, jc): # Then we found another junction, note down the distance between them
            distances[(jr, jc)][(r, c)] = d
            continue

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if 0 <= r + dr < R and 0 <= c + dc < C and grid[r + dr, c + dc] != '#' and (r + dr, c + dc) not in seen:
                steps.append((r + dr, c + dc, d + 1))

print(distances)
# now try all combinations and see which is longer
ml = 0
def dfs(point, distance, seen):
    global ml
    r, c = point

    if (r, c) in seen:
        return 

    if (r, c) == (er, ec):
        ml = max(ml, distance)
        return

    for (jr, jc), d in distances[(r,c)].items():
        if (jr, jc) not in seen:
            dfs((jr, jc), distance + d, seen | set([(r, c)]))

dfs((sr, sc), 0, set())
print(ml)
