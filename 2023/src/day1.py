#!/bin/env python3

digits = ["one", "two", "three", "four", "five",
          "six", "seven", "eight", "nine"]
with open(0) as file:
    vals = []
    for line in file.readlines():
        line = line.strip('\n')
        val = ""
        for i, c in enumerate(line):
            found = False
            if c.isdigit():
                val = val + c
                break
            for digit in digits:
                if digit in line[:i+1]:
                    val = val + str(digits.index(digit) + 1)
                    found = True
                    break
            if found:
                break
        for i, c in enumerate(reversed(line)):
            found = False
            if c.isdigit():
                val = val + c
                break
            for digit in digits:
                if digit in line[-i-1:]:
                    print(digit)
                    val = val + str(digits.index(digit) + 1)
                    found = True
                    break
            if found:
                break
        vals.append(int(val))

    print(sum(vals))
