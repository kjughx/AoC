#!/usr/bin/env python3
import numpy as np

lines = [line.strip() for line in open(0).readlines()]
r,c = 0,0
loop = []
length = 0
for line in lines:
    d, l, color = line.split(' ')

    l = int(l)
    if d == 'R':
        r,c = r, c + l
    elif d == 'L':
        r,c = r, c - l
    elif d == 'D':
        r,c = r + l, c
    elif d == 'U':
        r, c = r - l ,c

    length += l
    loop.append((r, c, color))

A = abs(sum(loop[i][0] * (loop[i - 1][1] - loop[(i + 1) % len(loop)][1]) for i in range(len(loop)))) // 2
print(length + (A - length// 2 + 1))


loop = []
length = 0
for line in lines:
    _, _, color = line.split(' ')
    color = int(color[2:-1], 16)
    d = color & 0xf
    l = color & 0xfffff0
    l >>= 4

    if d == 0:
        r,c = r, c + l
    elif d == 1:
        r,c = r + l, c
    elif d == 2:
        r,c = r, c - l
    elif d == 3:
        r, c = r - l ,c

    length += l
    loop.append((r, c, color))

A = abs(sum(loop[i][0] * (loop[i - 1][1] - loop[(i + 1) % len(loop)][1]) for i in range(len(loop)))) // 2
print(length + (A - length// 2 + 1))
