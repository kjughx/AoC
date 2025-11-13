#!/bin/env python3
from timer import profiler


@profiler
def solve(stones, n):
    for i in range(n):
        new = {}
        for stone, count in stones.items():
            if stone == 0:
                if 1 not in new:
                    new[1] = 0
                new[1] += count
            elif len(str(stone)) % 2 == 0:
                s = str(stone)
                s1, s2 = int(s[:len(s)//2]), int(s[len(s)//2:])
                if s1 not in new:
                    new[s1] = 0
                if s2 not in new:
                    new[s2] = 0
                new[s1] += count
                new[s2] += count
            else:
                c = stone * 2024
                if c not in new:
                    new[c] = 0
                new[c] += count
        stones = new

    s = 0
    for _, count in stones.items():
        s += count
    print(s)


with open(0) as file:
    stones = {int(i): 1 for i in file.readline().split(' ')}

    solve(stones, 25)
    solve(stones, 75)
