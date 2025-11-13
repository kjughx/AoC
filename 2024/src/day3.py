#!/bin/env python3
import re
from timer import profiler


def mul(a, b):
    return a * b


@profiler
def part1(lines):
    p = 0
    pattern = re.compile(r"mul\(([0-9]+),([0-9]+)\)")
    for line in lines:
        for a, b in re.findall(pattern, line):
            p += int(a) * int(b)
    print(p)


@profiler
def part2(lines):
    p = 0
    pattern = re.compile(r"mul\(([0-9]+),([0-9]+)\)|(don't\(\))|(do\(\))")
    do = True
    for line in lines:
        for a in re.findall(pattern, line):
            if a[2] == "don't()":
                do = False
                continue
            if a[3] == "do()":
                do = True
                continue
            if do:
                p += int(a[0]) * int(a[1])

    print(p)


with open(0) as file:
    lines = [line.strip('\n') for line in file.readlines()]
    part1(lines)
    part2(lines)
