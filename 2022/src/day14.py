import ast
import numpy as np
from collections import deque

with open(0) as file:
    lines = [[ast.literal_eval(point) for point in line.strip('\n').split(' -> ')] for line in file.readlines()]
    mx, zr = max([point[0] for line in lines for point in line]), min([point[0] for line in lines for point in line]),
    nr = max([point[1] for line in lines for point in line]) + 3

    for i, line in enumerate(lines):
        for j, point in enumerate(line):
            lines[i][j] = (point[0] - zr, point[1])

    nc = mx - zr + 1
    grid = [deque(['.' for x in range(nc)]) for y in range(nr)]

    for c in range(0, nc):
        grid[-1][c] = '#'

    for path in lines:
        for i, ps in enumerate(path[:-1]):
            pe = path[i+1]
            sc = ps[1] if ps[1] < pe[1] else pe[1]
            ec = pe[1] if pe[1] > ps[1] else ps[1]
            sr = ps[0] if ps[0] < pe[0] else pe[0]
            er = pe[0] if pe[0] > ps[0] else ps[0]
            for c in range(sc, ec+1):
                for r in range(sr, er+1):
                    grid[c][r] = '#'

    infinite = False
    ssx, ssy = (500 - zr, 0)
    while not infinite:
        sx, sy = ssx, ssy
        falling = True
        while falling:
            if grid[sy][sx] == '.':
                if sy + 1 < nr:
                    if grid[sy+1][sx] == '.':
                        sy += 1
                        continue
                    if (sx - 1 == -1):
                        for r in grid[:-1]:
                            r.appendleft('.')
                        grid[-1].appendleft('#')
                        sx += 1
                        ssx += 1
                        nc += 1
                    if grid[sy+1][sx-1] == '.':
                        sx -= 1
                        sy += 1
                        continue

                    if (sx + 1 == nc):
                        for r in grid[:-1]:
                            r.append('.')
                        grid[-1].append('#')
                        nc += 1
                    if grid[sy+1][sx+1] == '.':
                        sx += 1
                        sy += 1
                        continue
                    else:
                        grid[sy][sx] = 'o'
                        falling = False
            else:
                infinite = True
                break
    cp = 0
    for r in grid:
        for c in r:
            if c == 'o':
                cp += 1
        print("".join(r))

    print(cp)

