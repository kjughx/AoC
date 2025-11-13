import functools
import ast
def compare(x, y):
    def rec_cmp(x, y):
        match x, y:
            case int(x), int(y):
                if x < y: return 1
                elif x > y: return 2
                else: return 3
                    
            case int(x), list(y): return rec_cmp([x], y)
            case list(x), int(y): return rec_cmp(x, [y])
            case list(x), list(y):
                ret = -1
                for i in range(max(len(x), len(y))):
                    try:
                        ret = rec_cmp(x[i], y[i])
                    except:
                        if i == len(x): ret = 1
                        else: ret = 2
                    if ret == 1: return 1
                    if ret == 2: return 2
                return 3

    return rec_cmp(x, y) == 1

with open(0) as file:
    lines = [line.strip('\n') for line in file.readlines()]

    # part 1
    pid = 0
    count = 0 
    while pid < len(lines):
        left,right = ast.literal_eval(lines[pid]), ast.literal_eval(lines[pid+1])
        if compare(left, right):
            count += pid/3 + 1
        pid += 3
    print(count)
    
    # part 2
    lines = [line for line in lines if len(line) > 1]
    lines.append('[[2]]')
    lines.append('[[6]]')

    i = 0
    j = None
    while i < len(lines):
        j = i + 1
        while j < len(lines):
            if not compare(ast.literal_eval(lines[i]), ast.literal_eval(lines[j])):
                tmp = lines[i];
                lines[i] = lines[j];
                lines[j] = tmp
            j += 1
        i += 1

    dk = 1
    for i, val in enumerate(lines):
        if val == '[[2]]' or val == '[[6]]':
            dk *= (i+1)
    print(dk)

