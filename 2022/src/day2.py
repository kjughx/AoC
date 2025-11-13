file = open(0)

scores = { 'X': 1, 'Y': 2, 'Z': 3 }
lose = {'A': 'Z', 'B': 'X', 'C': 'Y'}
win = { 'A': 'Y', 'B': 'Z', 'C': 'X' }
draw = { 'A': 'X', 'B': 'Y', 'C': 'Z' }

score1 = 0
score2 = 0

for line in file.readlines():
    line = line.strip('\n')
    split = line.split(' ')
    opp = split[0]
    me = split[1]
    if opp == 'A':
        if me == 'Y':
            score1 += scores[me] + 6
        elif me == 'X':
            score1 += scores[me] + 3
        else:
            score1 += scores[me]
    if opp == 'B':
        if me == 'Z':
            score1 += scores[me] + 6
        elif me == 'Y':
            score1 += scores[me] + 3
        else:
            score1 += scores[me]
    if opp == 'C':
        if me == 'X':
            score1 += scores[me] + 6
        elif me == 'Z':
            score1 += scores[me] + 3
        else:
            score1 += scores[me]
    
    if me == 'X': # lose
        score2 += scores[lose[opp]]
    
    if me == 'Y': #draw
        score2 += scores[draw[opp]] + 3
    if me == 'Z': #win
        score2 += scores[win[opp]] + 6


print(score1)
print(score2)








