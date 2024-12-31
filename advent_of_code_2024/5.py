# I've read solution on reddit, but I cannot really understand them at the moment.
# So I'm trying to finish it just somehow with dirty code

rules = dict()
updates = list()
middle_page_sum = 0
middle_page_sum_2 = 0
incorrect_lines = list()

with open('5.txt', 'r') as f:
    updates_line = False
    while True:
        line = f.readline().strip()

        if not line:
            if not updates_line:
                updates_line = True
                continue
            else:
                break

        if updates_line:
            updates.append([int(i) for i in line.split(',')])
        else:
            a, b = [int(j) for j in line.split('|')]
            if a not in rules:
                rules[a] = list()
            rules[a].append(b)


def is_correct(update):
    for i in range(len(update)):
        a = update[i]

        if a not in rules and i != len(update) - 1:
            # Incorrect, because there should have been rules for this number, if it is not last in the line
            incorrect_lines.append(update)
            return False

        if a in rules:
            for j in range(i + 1, len(update)):
                rules_set = rules[a]
                if update[j] not in rules_set:
                    incorrect_lines.append(update)
                    return False

    return True


for update in updates:
    if is_correct(update):
        middle_page_sum += update[(len(update) // 2)]

# Part 1
print(middle_page_sum)


# Part 2
# Next function uses the code from this solution
# https://github.com/RD-Dev-29/advent_of_code_24/blob/main/code_files/day5.py#L66
# Wouldn't say I understand it fully at the moment
def fix_update(update):
    l, r = 0, 1
    while r < len(update):
        if update[r] in rules and set(rules[update[r]]).intersection([update[l]]):
            update[l], update[r] = update[r], update[l]
        r += 1
        if r == len(update):
            l += 1
            r = l + 1
    return update


for line in incorrect_lines:
    update = fix_update(line)
    middle_page_sum_2 += update[(len(update) // 2)]

print(middle_page_sum_2)
