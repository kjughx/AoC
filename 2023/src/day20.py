#!/usr/bin/env python3
from collections import deque
import math

lines = [line.strip() for line in open(0).readlines()]

modules = {'broadcaster': {'t': 'B', 'state': 0, 'inputs': {}, 'outputs': []}}

for line in lines:
    if 'broadcaster' in line:
        _,outputs = line.split(' -> ')
        for output in outputs.split(','):
            output = output.strip()
            if output not in modules:
                modules[output] = {'t': '', 'state': 0, 'inputs': {}, 'outputs': []}
            modules[output]['inputs']['broadcaster'] = 0
            modules['broadcaster']['outputs'].append(output)
        continue

    t = line[0]
    name,outputs = line[1:].split(' -> ')
    modules[name] = {'t': t, 'state': 0 if t == '%' else 1, 'inputs': {}, 'outputs': [output.strip() for output in outputs.split(',')]}

for name, module in modules.items():
    for output in module['outputs']:
        if output in modules and modules[output]['t'] == '&':
            modules[output]['inputs'][name] = 0

# inputs to 'dd':
inputs = [name for name,module in modules.items() if 'dd' in module['outputs']]
cycles = {iname: None for iname in inputs}

high, low = 0,0
i = 0
while True:
    i += 1
    pending = deque(('broadcaster', output, 0) for output in modules['broadcaster']['outputs'])
    low += 1

    while pending:
        iname, oname, signal = pending.popleft()
        if signal == 1:
            high += 1
        else:
            low += 1

        if oname == 'dd' and signal == 1: # then this is one of them
            if cycles[iname] is None:
                cycles[iname] = i
            if not any([cycle is None for cycle in cycles.values()]):
                gcf = 1
                for cycle in cycles.values():
                    gcf = int(gcf * cycle / (math.gcd(gcf, cycle)))
                print(gcf)
                exit(0)

        if oname not in modules:
            continue
        module = modules[oname]

        if module['t'] == '%':
            if signal == 0:
                module['state'] ^= 1
                pending += [(oname, output, module['state']) for output in module['outputs']]
        else:
            module['inputs'][iname] = signal
            module['state'] = 0 if all([v == 1 for v in module['inputs'].values()]) else 1
            pending += [(oname, output, module['state']) for output in module['outputs']]

"""
rx gets its signal from dd, who's a conjunction.
So dd will output low iff all of dd's inputs are high
so we need to figure out how long it takes for all of its inputs to go high.

Use the least common multiple to do this.
Need to record each of dd's inputs and how long they take to get to high.
Then once we know all of them, get the least common multiple of their cycles to get the answer.
"""

print(low * high)
