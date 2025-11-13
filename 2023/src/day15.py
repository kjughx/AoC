#!/bin/env python3

lines = [line.strip() for line in open(0).readlines()]
#
# t = 0
# for step in lines[0].split(','):
#     s = 0
#     for c in step:
#         s += ord(c)
#         s *= 17
#         s %= 256
#     t += s
# print(t)


from collections import OrderedDict
boxes = [OrderedDict() for _ in range(256)]

for label in lines[0].split(','):
    box = 0
    if '=' in label:
        label, focal_length = label.split('=')
        box = 0
        for c in label:
            box += ord(c)
            box *= 17
            box %= 256
        boxes[box][label] = focal_length
    if '-' in label:
        label, _ = label.split('-')
        box = 0
        for c in label:
            box += ord(c)
            box *= 17
            box %= 256
        if label in boxes[box]:
            boxes[box].pop(label)

t = 0
for i, box in enumerate(boxes):
    for j, label in enumerate(box):
        t += (i + 1) * (j + 1) * int(box[label])

print(t)
