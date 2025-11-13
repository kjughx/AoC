#!/bin/env python3
import re
import math
from itertools import cycle

lines = [line.strip() for line in open(0).readlines()]

LR = lines[0]
dirs = {}
start = []
for line in lines[2:]:
    a, b, c = re.findall(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)", line)[0]
    dirs[a] = (b, c)
    if a[-1] == 'A':
        start.append(a)

pos = 'AAA'
LR = [lr for lr in LR]
for i, lr in enumerate(cycle(LR)):
    pos = dirs[pos][0 if lr == 'L' else 1]

    if pos == 'ZZZ':
        print(i+1)
        break

# Find how long it takes for each start to find each Z
ns = []
for pos in start:
    n = 0
    for i, lr in enumerate(cycle(LR)):
        pos = dirs[pos][0 if lr == 'L' else 1]
        if pos[-1] == 'Z':
            ns.append(i + 1)
            break

# the lcm of them all is the total cycles it takes
gcf = 1
for n in ns:
    gcf = int(gcf * n / (math.gcd(gcf, n)))

print(gcf)
