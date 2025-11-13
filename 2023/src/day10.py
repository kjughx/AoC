#!/bin/env python3
import numpy as np

from collections import deque

grid = np.array([np.array([c for c in line.strip()]) for line in open(0).readlines()])
R = grid.shape[0]
C = grid.shape[1]

pipes = {'|': [(-1, 0), (1, 0)],
         '-': [(0, -1), (0, 1)],
         'L': [(-1, 0), (0, 1)],
         'J': [(-1, 0), (0, -1)],
         '7': [(0, -1), (1, 0)],
         'F': [(1, 0), (0, 1)]}


def connected(p1, p2):
    c = 0

    if grid[p1[0], p1[1]] == 'S':
        c += 1
    else:
        for r in pipes[grid[p1[0], p1[1]]]:
            if (p1[0] + r[0], p1[1] + r[1]) == p2:
                c += 1

    if grid[p2[0], p2[1]] == 'S':
        c += 1
    else:
        for r in pipes[grid[p2[0], p2[1]]]:
            if (p2[0] + r[0], p2[1] + r[1]) == p1:
                c += 1

    return c == 2

def neis(g, r, c):
    ls = []
    for i, j in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        if 0 <= r + i < R and 0 <= c + j < C:
            t = g[r + i, c + j]
            if t in pipes:
                if connected((r, c), (r+i, c + j)):
                    ls.append((r + i, c + j))
            if t == 'S':
                ls.append((r + i, c + j))
    return ls


ones = np.ones(grid.shape)

s0 = np.where(grid == 'S')
s = (s0[0][0], s0[1][0])

# find the length of the loop and divide by two.

news = deque([(0, (s[0], s[1]))])
loop = {(s[0], s[1])}

m = 0
while len(news) > 0:
    n, pos = news.popleft()
    if n > m:
        m = n
    ones[pos[0], pos[1]] = 0
    for nei in neis(grid, pos[0], pos[1]):
        if grid[nei[0], nei[1]] == 'S':
            continue
        if nei not in loop:
            news.append((n + 1, nei))
            loop.add(nei)
print(m)

# NOTE
"""
print(lines[s[0]-2:s[0]+4, s[1]-2:s[1]+4])
S is '|' in final answer
"""
grid[s[0], s[1]] = '|'

for r in range(R):
    for c in range(C):
        if (r, c) not in loop:
            grid[r, c] = "."

# If a point crosses the loop an even number of times to get the edge it is outside
# only 7F or JL because they're pipes with flat sides on the same side:
# 7F are horizontal at the top and JL are horizontal at the bottom.
"""
has opening:
  ....    ....
  .LJ.    .F7.
  .||.    .||.
  ....    ....

no opening:
  ....    ....
  .|..    ..|.
  .L7.    .FJ.
  ..|.    .|..
"""
os = np.where(ones == 1)
for i, j in zip(os[0], os[1]):
    if sum([c in "|7F" for c in grid[i, 0:j]]) % 2 == 0:
        ones[i, j] = 0

print(len(np.where(ones == 1)[0]))
