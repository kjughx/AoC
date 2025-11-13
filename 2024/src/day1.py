#!/bin/env python3

import numpy as np
from timer import profiler


@profiler
def part1(data):
    left = np.array([int(r.split("  ")[0]) for r in data])
    right = np.array([int(r.split("  ")[1]) for r in data])

    left = sorted(left)
    right = sorted(right)

    s = 0
    for a, b in zip(left, right):
        s += abs(a - b)

    print(s)  # part 1


@profiler
def part2(data):
    left = np.array([int(r.split("  ")[0]) for r in data])
    right = np.array([int(r.split("  ")[1]) for r in data])

    left = sorted(left)
    right = sorted(right)

    counts = {}
    for r in right:
        if r in counts:
            counts[r] += 1
        else:
            counts[r] = 1

    s = 0
    for l in left:
        if l in counts:
            s += l * counts[l]
    print(s)


with open(0) as f:
    data = f.readlines()
    part1(data)
    part2(data)
