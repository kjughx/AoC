#!/bin/env python3
import re
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib import cm
import random2


def evolve(x, y, vx, vy, t):
    x = (x + vx * t) % X
    y = (y + vy * t) % Y

    return (x, y)


with open(0) as file:
    robots = {tuple(map(int, re.findall(r"-?\d+", line)))
              for line in file.readlines()}
    Y = 103
    X = 101

    qs = [0 for _ in range(4)]
    for (x, y, vx, vy) in robots:
        x, y = evolve(x, y, vx, vy, 100)

        if 0 <= x < X // 2 and 0 <= y < Y // 2:  # top left
            qs[0] += 1
        elif 0 <= x < X // 2 and Y // 2 < y <= Y:  # bottom left
            qs[1] += 1
        elif X // 2 < x <= X and Y // 2 < y <= Y:  # bottom right
            qs[2] += 1
        elif X // 2 < x <= X and 0 <= y < Y // 2:  # top right
            qs[3] += 1

    p = 1
    for q in qs:
        p *= q
    print(p)

    fig = plt.figure()

    a = [[0 for _ in range(X)] for _ in range(Y)]
    im = plt.imshow(a, interpolation='none', aspect='auto', cmap=cm.jet, vmin=0, vmax=1)

    T = 0

    # def animate(i):
    #     global T
    #     grid = [[0 for _ in range(X)] for _ in range(Y)]
    #     for robot in robots:
    #         c, r = evolve(*robot, 6752)
    #         grid[r][c] = random2.random()
    #     T += 1
    #     im.set_array(grid)
    #     fig.suptitle(f"{T}")
    #     return [im]
    # ani = anim.FuncAnimation(fig, animate, frames=1000, interval=10)

    grid = [[0 for _ in range(X)] for _ in range(Y)]
    for robot in robots:
        c, r = evolve(*robot, 6752)
        grid[r][c] = random2.random()
    im.set_array(grid)
    plt.show()
