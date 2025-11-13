#!/bin/env python3

import re
import math

lines = open(0).readlines()
ts = list(map(int, re.findall(r"\d+", lines[0])))
ds = list(map(int, re.findall(r"\d+", lines[1])))

tss = []
for r, time in enumerate(ts):
    md = ds[r]
    cnt = 0
    for t in range(time):
        d = t*(time-t)
        if d > md:
            cnt += 1
    tss.append(cnt)
print(math.prod(tss))
