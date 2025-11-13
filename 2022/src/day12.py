import numpy as np
with open(0) as file:
    grid = [[c for c in line.strip('\n')] for line in file.readlines()]
    for x, r in enumerate(grid):
        for y, c in enumerate(grid[x]):
            if c == 'S':
                sx, sy = x, y
                grid[x][y] = 'a'
            elif c == 'E':
                ex, ey = x, y
                grid[x][y] = 'z'

    nnx = len(grid)
    nny = len(grid[0])

    start = []
    for x, r in enumerate(grid):
        for y, c in enumerate(r):
            if c == 'a':
                start.append((x, y))

    min = 468
    pspt = {}
    for i, (sx, sy) in enumerate(start):
        spt = {(sx, sy): 0}
        found = False
        br = False 
        while True:
            for cx, cy in list(spt.keys()).copy():
                for dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nx, ny = cx + dir[0], cy + dir[1]
                    if (nx < 0 or nx >= nnx) or (ny < 0 or ny >= nny):
                        continue

                    if ord(grid[nx][ny]) - ord(grid[cx][cy]) > 1:
                        continue

                    if (nx, ny) == (ex, ey):
                        print(spt[(cx, cy)] + 1)
                        found=True
                        min = spt[(cx, cy)] + 1
                        break

                    if spt[(cx, cy)] + 1 > min:
                        br = True
                        break

                    if not (nx, ny) in spt:
                        spt[(nx, ny)] = spt[(cx, cy)] + 1
                del spt[(cx, cy)]

            if found:
                break
            if br:
                break

