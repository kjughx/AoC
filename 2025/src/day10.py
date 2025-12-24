#!/usr/bin/env python3

import math
import sys
import re
import numpy as np
from pulp import LpProblem, LpVariable, lpSum, LpInteger, LpStatus, value

def main(data):
    n= 0
    for m, line in enumerate(data.splitlines()):
        _buttons, counts = re.findall(r"\[.*\] (.*) \{(.*)\}", line)[0]
        counts = np.array(eval(f"[{counts}]"))
        buttons = []
        for i, button in enumerate(_buttons.split(' ')):
            button = re.sub(r"\(", "[", button)
            button = re.sub(r"\)", "]", button)
            buttons.append(eval(button))

        A = np.zeros((len(counts), len(buttons)), dtype=int)
        for i, button in enumerate(buttons):
            for j in button:
                A[j, i] = 1

        problem = LpProblem("Solution", sense=1)
        variables = [LpVariable(f"x{i}", lowBound=0, cat=LpInteger) for i in range(len(buttons))]
        for i in range(len(counts)):
            problem += lpSum(A[i, j] * variables[j] for j in range(len(variables))) == counts[i]
        problem += lpSum(variables)
        problem.solve()

        n += sum(map(value, variables))
    print(n)

if __name__ == "__main__":
    main(sys.stdin.read())
