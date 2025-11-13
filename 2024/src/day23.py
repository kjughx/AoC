#!/bin/env python3
import networkx as nx
from timer import profiler

# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,C0200,E0001

lines = [line.strip() for line in open(0).readlines()]


@profiler
def part1(lines):
    G = nx.Graph()

    edges = {}
    for line in lines:
        a, b = line.split('-')
        a, b = sorted([a, b])

        G.add_edge(a, b)

    groups = [clique for clique in nx.enumerate_all_cliques(
        G) if len(clique) == 3]

    p = 0
    for group in groups:
        for c in group:
            if c[0] == 't':
                p += 1
                break
    print(p)


@profiler
def part2(lines):
    G = nx.Graph()

    edges = {}
    for line in lines:
        a, b = line.split('-')
        a, b = sorted([a, b])

        G.add_edge(a, b)

    groups = [clique for clique in nx.enumerate_all_cliques(
        G) if len(clique) == 3]

    m = 0
    mc = None
    for clique in nx.enumerate_all_cliques(G):
        if len(clique) > m:
            m = len(clique)
            mc = clique

    print(",".join(sorted(mc)))


part1(lines)
part2(lines)
