#!/bin/env python3

lines = [line.strip() for line in open(0).readlines()]

seen = {}
def f(springs, sizes, block = False):
    if len(springs) == 0:
        return sum(sizes) == 0

    if sum(sizes) == 0:
        return '#' not in springs

    s = (springs, sizes)
    if s in seen:
        return seen[s]

    ret = 0
    if springs[0] in '.?':
        if block:
            if sizes[0] == 0:
                ret += f(springs[1:], sizes[1:], False)
        else:
            ret += f(springs[1:], sizes, False)

    if springs[0] in '#?':
        if sizes[0] > 0:
            ret += f(springs[1:], (sizes[0] - 1, *sizes[1:]), True)

    seen[s] = ret
    return ret


# part 1: 7732
# t = 0
# for line in lines:
#     springs, sizes = line.split(" ")
#     sizes = list(map(int, sizes.split(",")))
#     t += f(springs, sizes)
# print(t)

# part2:
t = 0
for i, line in enumerate(lines):
    springs, sizes = line.split(" ")
    sizes = tuple(map(int, sizes.split(",")))
    springs = "?".join([springs for _ in range(5)])
    t += f(springs, 5*sizes)

    seen = {}
# 3277341243133 too low
print(t)
