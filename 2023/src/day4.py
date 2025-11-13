#!/bin/env python3

myc = []
cards = []

with open(0) as file:
    for line in file.readlines():
        line = line.strip('\n')
        card, nbrs = line.split(" | ")
        myc.append([int(nbr) for nbr in nbrs.split(" ") if len(nbr) > 0])

        card = card.split(": ")[1]

        cards.append([int(card) for card in card.split(" ") if len(card) > 0])

t = 0
for i, card in enumerate(cards):
    points = 0
    for nbr in card:
        if nbr in myc[i]:
            if points == 0:
                points = 1
            else:
                points *= 2
    t += points

copies={(i+1) : 0 for i,_ in enumerate(cards)}
for i, card in enumerate(cards):
    points = 0
    for nbr in card:
        if nbr in myc[i]:
            points += 1

    for point in range(1, points + 1):
        p = (i+1) + point
        if p in copies:
            copies[p] += 1 + copies[i+1]
        else:
            copies[p] = 1

t2 = 0
for key,val in copies.items():
    t2 += val + 1

print(t)
print(t2)
