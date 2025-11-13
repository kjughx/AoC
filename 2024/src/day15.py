#!/bin/env python3
import numpy as np
from timer import profiler


def to_dir(c):
    if c == '^':
        return (-1, 0)
    elif c == '>':
        return (0, 1)
    elif c == 'v':
        return (1, 0)
    elif c == '<':
        return (0, -1)
    else:
        assert False


def push(grid, r, c, dr, dc, boxes):
    nr, nc = r + dr, c + dc
    if grid[nr, nc] == '#':
        return []
    elif grid[nr, nc] == 'O':
        return push(grid, nr, nc, dr, dc, boxes + [(nr, nc)])
    elif grid[nr, nc] == '.':
        return boxes
    else:
        assert False


def pushud(grid, r, c, dr, boxes):
    nr, nc = r + dr, c
    if grid[nr, nc] == '#' or grid[nr, nc + 1] == '#':
        return []

    if grid[nr, nc] == '.' and grid[nr, nc + 1] == '.':
        return boxes

    n = set(boxes)
    if grid[nr, nc] == '[':
        p = pushud(grid, nr, nc, dr, boxes + [(nr, nc)])
        if not p:
            return []
        n |= set(p)
    elif grid[nr, nc] == ']':
        p = pushud(grid, nr, nc - 1, dr, boxes + [(nr, nc - 1)])
        if not p:
            return []
        n |= set(p)

    if grid[nr, nc + 1] == '[':
        p = pushud(grid, nr, nc + 1, dr, boxes + [(nr, nc + 1)])
        if not p:
            return []
        n |= set(p)
    elif grid[nr, nc + 1] == ']':
        p = pushud(grid, nr, nc, dr, boxes + [(nr, nc)])
        if not p:
            return []
        n |= set(p)

    return n


def pushrl(grid, r, c, dc, boxes):
    nr, nc = r, c + dc
    if grid[nr, nc] == '#' or grid[nr, nc + 1] == '#':
        return []
    if dc == 1:
        if grid[nr, nc + 1] == '[':
            return pushrl(grid, nr, nc + 1, dc, boxes + [(nr, nc + 1)])
        if grid[nr, nc + 1] == '.':
            return boxes

    if dc == -1:
        if grid[nr, nc] == ']':
            return pushrl(grid, nr, nc - 1, dc, boxes + [(nr, nc - 1)])
        if grid[nr, nc] == '.':
            return boxes

    assert False


@profiler
def part1(grid):
    grid = np.array([list(row) for row in grid.split('\n')])
    walls = np.where(grid == '#')
    walls = {(r, c) for r, c in zip(walls[0], walls[1])}
    boxes = np.where(grid == 'O')
    boxes = {(r, c) for r, c in zip(boxes[0], boxes[1])}

    pos = np.where(grid == '@')
    r, c = pos[0][0], pos[1][0]
    grid[r, c] = '.'
    for move in moves:
        dr, dc = to_dir(move)
        nr, nc = r + dr, c + dc
        if (nr, nc) in walls:
            continue
        elif grid[nr, nc] == '.':
            r, c = nr, nc
            continue
        elif grid[nr, nc] == 'O':
            to_push = push(grid, nr, nc, dr, dc, [(nr, nc)])
            if to_push:
                grid[*to_push[0]] = '.'
                for r, c in to_push:
                    grid[r + dr, c + dc] = 'O'
                r, c = nr, nc
        else:
            print(grid[nr, nc])
            assert False

    boxes = np.where(grid == 'O')
    p = 0
    for r, c in zip(boxes[0], boxes[1]):
        p += 100 * r + c
    print(p)


@profiler
def part2(_grid):
    grid = []
    for row in _grid.split('\n'):
        nrow = []
        for c in row:
            if c == '@':
                nrow += ['@', '.']
            elif c == 'O':
                nrow += ['[', ']']
            else:
                nrow += 2*[c]
        grid.append(nrow)
    grid = np.array(grid)

    walls = np.where(grid == '#')
    walls = {(r, c) for r, c in zip(walls[0], walls[1])}

    pos = np.where(grid == '@')
    r, c = pos[0][0], pos[1][0]
    grid[r, c] = '.'

    for i, move in enumerate(moves):
        dr, dc = to_dir(move)
        nr, nc = r + dr, c + dc
        if (nr, nc) in walls:
            continue
        elif grid[nr, nc] == '.':
            r, c = nr, nc
        elif grid[nr, nc] in '[]':
            to_push = []
            if move in '^v':
                to_push = pushud(grid, nr, nc, dr, [(nr, nc)]) if grid[nr, nc] == '[' else pushud(
                    grid, nr, nc - 1, dr, [(nr, nc - 1)])
            elif move == '>':
                to_push = pushrl(grid, nr, nc, dc, [(nr, nc)])
            elif move == '<':
                to_push = pushrl(grid, nr, nc - 1, dc, [(nr, nc - 1)])

            if to_push:
                for r, c in to_push:
                    grid[r, c] = '.'
                    grid[r, c + 1] = '.'
                for r, c in to_push:
                    grid[r + dr, c + dc] = '['
                    grid[r + dr, c + dc + 1] = ']'

                r, c = nr, nc
        else:
            print(grid[nr, nc])
            assert False

    boxes = np.where(grid == '[')
    p = 0
    for r, c in zip(boxes[0], boxes[1]):
        p += 100 * r + c
    print(p)


with open(0) as file:
    grid, moves = file.read().split('\n\n')
    moves = [move for move in moves if move != '\n']

    part1(grid)
    part2(grid)
