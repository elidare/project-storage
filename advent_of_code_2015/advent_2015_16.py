import re


with open('16.txt', 'r') as f:
    input = [a.strip() for a in f.readlines()]

aunts = list()

for i in input:
    attributes = [atr.strip() for atr in re.sub('Sue \\d+:', '', i).split(',')]
    aunts.append({atr.split(':')[0]: int(atr.split(':')[1].strip()) for atr in attributes})

EXAMPLE = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1
}


def part_one():
    for j in range(len(aunts)):
        possible = True
        for k, v in aunts[j].items():
            if EXAMPLE[k] != v:
                possible = False

        if possible:
            return j + 1  # Because Aunt number is 1-based


def part_two():
    for j in range(len(aunts)):
        possible = True
        for k, v in aunts[j].items():
            if k in ['cats', 'trees'] and EXAMPLE[k] >= v:
                possible = False
            elif k in ['pomeranians', 'goldfish'] and EXAMPLE[k] <= v:
                possible = False
            elif k not in ['cats', 'trees', 'pomeranians', 'goldfish'] and EXAMPLE[k] != v:
                possible = False

        if possible:
            # Assuming only one Aunt is the right one
            return j + 1  # Because Aunt number is 1-based


print(part_one())
print(part_two())
