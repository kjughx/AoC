#!/bin/env python3
import re
from collections import defaultdict
from graphviz import Digraph

# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,C0200,E0001

lines = open(0).read()


def show():
    dot = Digraph()
    for i, (a, op, b, c) in enumerate(ops):
        dot.node(a, a)
        dot.node(b, b)
        dot.node(c, c)
        dot.node(str(i), op, shape='circle')
        dot.edge(a, str(i))
        dot.edge(b, str(i))
        dot.edge(str(i), c)

    dot.render('graph', format='png', view=True)


bits = {}
for line in lines.split('\n\n')[0].split('\n'):
    bit, val = line.split(": ")
    bits[bit] = int(val)

unfinished = defaultdict(list)


def do_op(a, op, b, c):
    def opr(a, op, b):
        if op == 'AND':
            return a & b
        if op == 'OR':
            return a | b
        if op == 'XOR':
            return int(a != b)
        assert False

    if a not in bits or b not in bits:
        if a not in bits:
            unfinished[a] += [(a, op, b, c)]
        if b not in bits:
            unfinished[b] += [(a, op, b, c)]
        return

    bits[c] = opr(bits[a], op, bits[b])

    if c in unfinished:
        for a, op, b, c in unfinished.pop(c):
            do_op(a, op, b, c)


ops = [re.findall(r"([A-Za-z0-9]+)", line)
       for line in lines.split('\n\n')[1].strip().split('\n')]
gates = {}
inputs = {}
for a, op, b, c in ops:
    do_op(a, op, b, c)
    a, b = sorted([a, b])
    gates[(a, op, b)] = c
    gates[(b, op, a)] = c
    inputs[(a, b)] = op
    inputs[(b, a)] = op

Z = list(sorted(filter(lambda x: x[0] == 'z', bits), reverse=True))
output = [str(bits[z]) for z in Z]
print(int("".join(output), 2))

Z = list(sorted(filter(lambda x: x[0] == 'z', bits), reverse=False))

show()


cin = 'prt'
# This will print the first z that's incorrect
for z in Z[1:-1]:
    i = z.split('z')[1]
    carry1 = gates['x' + i, 'AND', 'y' + i]
    inter_sum = gates['x' + i, 'XOR', 'y' + i]
    try:
        op = inputs[cin, inter_sum]
        if op != 'AND' and op != 'XOR':
            print(op)
        carry2 = gates[cin, 'AND', inter_sum]
        sum = gates[inter_sum, 'XOR', cin]
        op = inputs[carry1, carry2]
        if op != 'OR':
            print(op)
        cout = gates[carry1, 'OR', carry2]

        if sum[0] != 'z':
            print(1, sum)
    except KeyError:
        print(z)
        continue
    if sum != z:
        print(z)

    cin = cout

wrong = ",".join(
    sorted(['z16', 'fkb', 'rqf', 'nnr', 'z31', 'rdn', 'z37', 'rrn']))
print(wrong)
