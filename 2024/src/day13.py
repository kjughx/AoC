#!/bin/env python3
import re
from timer import profiler


@profiler
def part1(lines):
    p = 0
    for l in range(0, len(lines), 4):
        ax, ay = list(
            map(int, re.findall(r"Button A: X\+([0-9]+), Y\+([0-9]+)", lines[l])[0]))
        bx, by = list(
            map(int, re.findall(r"Button B: X\+([0-9]+), Y\+([0-9]+)", lines[l + 1])[0]))
        px, py = list(
            map(int, re.findall(r"Prize: X=([0-9]+), Y=([0-9]+)", lines[l + 2])[0]))

        b = (py * ax - px * ay) / (ax * by - bx * ay)
        a = (px - b * bx) / ax

        if a.is_integer() and b.is_integer():
            p += 3 * a + b

    print(p)


@profiler
def part2(lines):
    p = 0
    for l in range(0, len(lines), 4):
        ax, ay = list(
            map(int, re.findall(r"Button A: X\+([0-9]+), Y\+([0-9]+)", lines[l])[0]))
        bx, by = list(
            map(int, re.findall(r"Button B: X\+([0-9]+), Y\+([0-9]+)", lines[l + 1])[0]))
        px, py = list(
            map(int, re.findall(r"Prize: X=([0-9]+), Y=([0-9]+)", lines[l + 2])[0]))

        px += 10000000000000
        py += 10000000000000

        b = (py * ax - px * ay) / (ax * by - bx * ay)
        a = (px - b * bx) / ax

        if a.is_integer() and b.is_integer():
            p += 3 * a + b

    print(p)


with open(0) as file:
    p = 0

    lines = [line for line in file.readlines()]

    part1(lines)
    part2(lines)
