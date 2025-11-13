#!/usr/bin/env python3
import re

workflows, starts = open(0).read().split('\n\n')

rules = {}
for wf in workflows.split('\n'):
    name, wf = wf.split('{')
    rules[name] = wf.strip('}')

t = 0
for start in starts.split('\n')[:-1]:
    x, m, a, s = map(int, re.findall(r"\d+", start))

    rule = "in"
    while rule not in "AR":
        if rule in rules:
            rule = rules[rule]

        cond, rule = rule.split(':', 1)
        if eval(cond):
            rule,  _ = rule.split(',', 1)
        else:
            _, rule = rule.split(',', 1)
    if rule == 'A':
        t += x + m + a + s
print(t)


from collections import deque
import math

wfs = deque([("in", {'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)})])

t = 0
i = 0
while wfs:
    i += 1
    rule, xmas = wfs.popleft()
    if rule in rules:
        rule = rules[rule]

    if rule in 'AR':
        if rule == 'A':
            p = 1
            for lo, hi in xmas.values():
                p *= (hi - lo) + 1
            t += p
        continue

    cond, rule = rule.split(':', 1)

    rule = rule.split(',', 1)
    k, c, v = cond[0], cond[1], int(cond[2:])

    if c == '<':
        true = (rule[0], {**xmas, k: (xmas[k][0], min(xmas[k][1], v - 1))})
        false = (rule[1], {**xmas, k: (max(xmas[k][0], v), xmas[k][1])})
    else:
        true = (rule[0], {**xmas, k: (max(xmas[k][0], v + 1), xmas[k][1])})
        false = (rule[1], {**xmas, k: (xmas[k][0], min(xmas[k][1], v))})

    if true[1][k][0] <= true[1][k][1]:
        wfs.append(true)
    if false[1][k][0] <= false[1][k][1]:
        wfs.append(false)

print(t)
