#!/usr/bin/env python3

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import sys
import re
from itertools import permutations

reds = {}
rows = {}
greens = set()

def is_inside(ps):
    def _is_inside(p):
        if p in reds or p in greens: return True
        x,y = p
        if y not in rows: return False
        return rows[y][0] <= x <= rows[y][1]

    if not all(map(_is_inside, ps)): return False

    for i in range(len(ps)):
        p0 = ps[i]
        p1 = ps[(i + 1) % len(ps)]
        if p0[0] == p1[0]:
            x = p0[0]
            for y in range(min(p0[1], p1[1]), max(p0[1], p1[1])):
                if not _is_inside((x,y)): return False
        else:
            y = p0[1]
            for x in range(min(p0[0], p1[0]), max(p0[0], p1[0])):
                if not _is_inside((x,y)): return False
    return True


def main(data):
    global reds, greens, rows
    points = []
    for line in data.splitlines():
        x, y = map(int, re.findall(r"\d+", line))
        points.append((x, y))

    reds = set(points)
    for i in range(len(points)):
        p0 = points[i]
        p1 = points[(i + 1) % len(points)]
        if p0[0] == p1[0]:
            greens |= {(p0[0], y) for y in range(min(p0[1], p1[1]), max(p0[1], p1[1]) + 1)}
        else:
            greens |= {(x, p0[1]) for x in range(min(p0[0], p1[0]), max(p0[0], p1[0]) + 1)}

    sorted_greens = (sorted(greens, key=lambda x: (x[1], x[0])))
    for g in sorted_greens:
        if g[1] not in rows:
            rows[g[1]] = (g[0], g[0])
            continue
        rows[g[1]] = (rows[g[1]][0], g[0])

    part1 = 0
    part2 = 0
    for r1,r2 in permutations(reds, 2):
        if r2[0] == r1[0] or r2[1] == r1[1]: continue
        r3 = (r1[0], r2[1])
        r4 = (r2[0], r1[1])

        area = (abs(r1[0] - r2[0]) + 1) * (abs(r1[1] - r2[1]) + 1)


        if area > part2 and is_inside([r1,r3,r2,r4]):
            part2 = area
        if area > part1:
            part1 = area


    print(part1, part2)
if __name__ == "__main__":
    main(sys.stdin.read())
