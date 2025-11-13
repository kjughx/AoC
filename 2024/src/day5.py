#!/bin/env python3
from timer import profiler


def valid(row, rules):
    for rule in rules:
        r1, r2 = rule
        if r1 in row and r2 in row:
            if row.index(r1) > row.index(r2):
                return False
    return True


def swap(row, rules):
    for rule in rules:
        r1, r2 = rule
        if r1 in row and r2 in row:
            if row.index(r1) > row.index(r2):
                row[row.index(r1)] = r2
                row[row.index(r2)] = r1
                return True, row
    return False, row


@profiler
def part1(rows, rules):
    p = 0
    for row in rows:
        if valid(row, rules):
            p += int(row[len(row) // 2])
    print(p)


@profiler
def part2(rows, rules):
    p = 0
    for row in rows:
        valid = True
        while True:
            swapped, row = swap(row, rules)
            if not swapped:
                break
            valid = False

        if not valid:
            p += int(row[len(row) // 2])
    print(p)


with open(0) as file:
    rules, rows = file.read().split('\n\n')
    rules = [rule.strip().split('|') for rule in rules.split('\n')]
    rows = [row.strip().split(',') for row in rows.split('\n')[:-1]]

    part1(rows, rules)
    part2(rows, rules)
