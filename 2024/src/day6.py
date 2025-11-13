#!/bin/env python3
import numpy as np
from copy import deepcopy

from timer import profiler


def inbounds(rc):
    if rc[0, 0] < 0 or rc[0, 0] >= R:
        return False

    if rc[1, 0] < 0 or rc[1, 0] >= R:
        return False

    return True


def key(rc, drdc):
    return tuple(map(int, (rc[0, 0], rc[1, 0], drdc[0, 0], drdc[1, 0])))


def walk(rc, grid):
    drdc = np.array([-1, 0])
    drdc.shape = (2, 1)

    rot = np.matrix([[0, 1], [-1, 0]])

    vis = set()
    vis.add(key(rc, drdc))
    while True:
        nrc = rc + drdc
        if not inbounds(nrc):
            break
        nkey = key(nrc, drdc)
        if nkey in vis:  # loop
            return False, vis
        vis.add(key(nrc, drdc))

        if grid[nrc[0, 0], nrc[1, 0]] != '#':
            rc = nrc
            continue

        drdc = rot * drdc
    return True, vis


@profiler
def part1(grid):
    print(len(walk(rc, grid)[1]) - 4)  # part 1


@profiler
def part2(grid):
    loops = 0
    for i in range(np.shape(grid)[0]):
        for j in range(np.shape(grid)[1]):
            ngrid = deepcopy(grid)
            ngrid[i, j] = '#'
            loops += not walk(rc, ngrid)[0]
    print(loops)


with open(0) as file:
    grid = np.matrix([[a for a in row.strip('\n')]
                     for row in file.readlines()])

    rc = np.array(np.where(grid == "^"))[:, 0]
    rc.shape = (2, 1)
    R, C = np.shape(grid)
    grid[rc[0], rc[0]] = '.'

    part1(grid)
    part2(grid)
