from itertools import combinations


with open('17.txt', 'r') as f:
    input = [int(a.strip()) for a in f.readlines()]
    TOTAL = 25


def part_one():
    possible_combos_total = list()
    for i in range(1, len(input) + 1):
        possible_combos = list(combinations(input, i))
        possible_combos_total += list(filter(lambda x: sum(x) == TOTAL, possible_combos))

    return len(possible_combos_total)


def part_two():
    possible_combos_total = list()
    min_containers = len(input)
    for i in range(1, len(input) + 1):
        possible_combos = list(combinations(input, i))

        for combo in possible_combos:
            if sum(combo) == TOTAL:
                min_containers = min(min_containers, len(combo))
                possible_combos_total.append(combo)

    possible_combos_total = list(filter(lambda x: len(x) == min_containers, possible_combos_total))
    return len(possible_combos_total)


print(part_one())
print(part_two())
