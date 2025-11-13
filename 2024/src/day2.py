#!/bin/env python3
from timer import profiler


def is_decreasing(lst):
    for a in range(1, len(lst)):
        if lst[a] > lst[a-1]:
            return False
    return True


def is_ascending(lst):
    for a in range(1, len(lst)):
        if lst[a] < lst[a-1]:
            return False
    return True


@profiler
def part1(lines):
    def is_safe(lst):
        safe = is_ascending(lst) or is_decreasing(lst)

        j = line[0]
        for i in lst[1::]:
            if not (1 <= abs(i - j) <= 3):
                safe = False
                break
            j = i

        return safe

    p = 0
    for line in lines:
        p += 1 if is_safe(line) else 0

    print(p)


@profiler
def part2(lines):
    def is_safe(lst, first=True):
        j = lst[0]

        safe = False

        safe = is_ascending(lst) or is_decreasing(lst)
        for i in lst[1::]:
            if not (1 <= abs(i - j) <= 3):
                safe = False
                break
            j = i
        else:
            safe &= True
        if not safe and first:
            for i in range(len(lst)):
                new = [j for j in lst]
                del new[i]
                safe = is_safe(new, False)
                if safe:
                    return safe

        return safe

    p = 0
    for line in lines:
        p += 1 if is_safe(line) else 0

    print(p)


with open(0) as file:
    lines = [list(map(int, line.strip('\n').split(' ')))
             for line in file.readlines()]
    part1(lines)
    part2(lines)
