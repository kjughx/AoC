file = open(0)

elf_cal = []

calories = 0
for line in file.readlines():
    line = line.strip('\n')
    if len(line) > 0:
        calories += int(line)
    else:
        elf_cal.append(calories)
        calories = 0

print(sorted(elf_cal))
