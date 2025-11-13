#!/bin/env python3
from collections import deque
from timer import profiler


@profiler
def part1(lines):
    p = 0
    for line in lines:
        result, eq = line.split(": ")
        eq = list(map(int, eq.split(' ')))
        result = int(result)

        q = deque([(eq[0], '+'), (eq[0], '*'), (eq[0], '||')])
        for i in range(1, len(eq)):
            nq = deque([])
            while q:
                a, op = q.popleft()
                if op == '+':
                    b = a + eq[i]
                    if b <= result:
                        nq.append((b, '+'))
                        nq.append((b, '*'))
                if op == '*':
                    b = a * eq[i]
                    if b <= result:
                        nq.append((b, '+'))
                        nq.append((b, '*'))
            q = nq
        for a, op in q:
            if a == result:
                p += a
                break
    print(p)


@profiler
def part2(lines):
    p = 0
    for line in lines:
        result, eq = line.split(": ")
        eq = list(map(int, eq.split(' ')))
        result = int(result)

        q = deque([(eq[0], '+'), (eq[0], '*'), (eq[0], '||')])
        for i in range(1, len(eq)):
            nq = deque([])
            while q:
                a, op = q.popleft()
                if op == '+':
                    b = a + eq[i]
                    if b <= result:
                        nq.append((b, '+'))
                        nq.append((b, '*'))
                        nq.append((b, '||'))
                if op == '*':
                    b = a * eq[i]
                    if b <= result:
                        nq.append((b, '+'))
                        nq.append((b, '*'))
                        nq.append((b, '||'))
                if op == '||':
                    b = int(str(a) + str(eq[i]))
                    if b <= result:
                        nq.append((b, '+'))
                        nq.append((b, '*'))
                        nq.append((b, '||'))
            q = nq
        for a, op in q:
            if a == result:
                p += a
                break
    print(p)


with open(0) as file:

    lines = [line.strip() for line in file.readlines()]
    part1(lines)
    part2(lines)
