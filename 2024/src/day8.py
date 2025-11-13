#!/bin/env python3
from timer import profiler


def slice(a, r, dr, c, dc, s):
    ret = []
    try:
        for t in range(s):
            if r + dr * t < 0:
                raise IndexError
            if c + dc * t < 0:
                raise IndexError

            ret.append((r + dr*t, c + dc*t))
        return ret
    except IndexError:
        return ret


def distance(a, b):
    ra, ca = a
    rb, cb = b
    return (ra-rb, ca-cb)


def inbounds(r, c):
    if r < 0 or r >= R:
        return False

    if c < 0 or c >= C:
        return False

    return True


@profiler
def part1(antennas):
    positions = set()
    for _, tan in antennas.items():
        for ra, ca in tan:
            for rb, cb in tan:
                if (ra, ca) == (rb, cb):
                    continue
                dr, dc = distance((ra, ca), (rb, cb))
                if inbounds(ra + dr, ca + dc):
                    positions.add((ra + dr, ca + dc))
                if inbounds(rb - dr, cb - dc):
                    positions.add((rb - dr, cb - dc))

    print(len(positions))


@profiler
def part2(antennas):
    positions = set()
    for _, tan in antennas.items():
        for ra, ca in tan:
            for rb, cb in tan:
                if (ra, ca) == (rb, cb):
                    continue
                dr, dc = distance((ra, ca), (rb, cb))
                if inbounds(ra + dr, ca + dc):
                    positions.add((ra + dr, ca + dc))
                if inbounds(rb - dr, cb - dc):
                    positions.add((rb - dr, cb - dc))

                positions.add((ra, ca))
                positions.add((rb, cb))

                for r, c in slice(grid, ra, dr, ca, dc, len(grid)):
                    if inbounds(r, c):
                        positions.add((r, c))
                for r, c in slice(grid, rb, -dr, cb, -dc, len(grid[0])):
                    if inbounds(r, c):
                        positions.add((r, c))

    print(len(positions))


with open(0) as file:
    grid = [[c for c in line.strip()] for line in file.readlines()]
    R, C = (len(grid), len(grid[0]))
    antennas = {}
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c].isalnum():
                antenna = grid[r][c]
                if antenna not in antennas:
                    antennas[antenna] = []
                antennas[antenna].append((r, c))

    part1(antennas)
    part2(antennas)
