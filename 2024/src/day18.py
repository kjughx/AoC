#!/bin/env python3
import heapq
from timer import profiler

def walk(fr, fc, corr):
    q = [(0, 0, 0)]
    m = R ** 2
    vis = {}
    while q:
        r, c, n = heapq.heappop(q)

        if (r, c) in vis and vis[(r, c)] <= n:
            continue

        vis[(r, c)] = n

        if (r, c) == (fr, fc):
            m = n
            break

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < R and 0 <= nc < C):
                continue

            if (nr, nc) in vis and vis[(nr, nc)] < n + 1:
                continue

            if (nr, nc) in corr:
                continue

            heapq.heappush(q, (nr, nc, n + 1))
    return m

@profiler
def part1():
    R = 71
    C = 71
    grid = [['.' for _ in range(R)] for _ in range(R)]

    corr = [(r, c) for r, c in bs[:1024]]
    print(walk(R - 1, C - 1, corr))

with open(0) as file:
    bs = [tuple(map(int, line.strip('\n').split(',')))
          for line in file.readlines()]
    bs = [(c, r) for r, c in bs]

    R = 71
    C = 71
    grid = [['.' for _ in range(R)] for _ in range(R)]

    corr = [(r, c) for r, c in bs[:1024]]
    print(walk(R - 1, C - 1, corr))

    ispath = True
    r = (1024, 3450)
    while True:
        low, high = r

        if low == high - 1:
            break

        mid = r[0] + (r[1] - r[0]) // 2
        rmid = walk(R - 1, C - 1, [(r, c) for r, c in bs[:mid]])
        if rmid != R ** 2:
            r = (mid, high)
        else:
            r = (low, mid)

    c, r = bs[r[0]]
    print(r, c)

