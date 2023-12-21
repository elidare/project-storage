# Part 1 is completely mine
# For Part 2 I carefully read through this solution and tried to do the same
# https://github.com/mgtezak/Advent_of_Code/blob/master/2023/Day_19.py
import math


with open('19.txt', 'r') as f:
    rules, parts = [items.split('\n') for items in f.read().split('\n\n')]
    rules = {rule.split('{')[0]: rule.split('{')[1][:-1] for rule in rules}
    parts = [{item.split('=')[0]: int(item.split('=')[1]) for item in part[1:-1].split(',')} for part in parts]
    accepted = []

    # Part 1
    def go_next(part, rule_set):
        rule = rule_set.split(',')
        if len(rule) == 1:
            return rule[0]
        condition, next_step = rule[0].split(':')[0], rule[0].split(':')[1]
        condition_more, condition_less = condition.split('>'), condition.split('<')
        if len(condition_more) > 1 and part[condition_more[0]] > int(condition_more[1]) or \
                len(condition_less) > 1 and part[condition_less[0]] < int(condition_less[1]):
            return next_step
        return go_next(part, ','.join(rule[1:]))

    for part in parts:
        next_step = 'in'
        while True:
            next_step = go_next(part, rules[next_step])
            if next_step in ('A', 'R'):
                if next_step == 'A':
                    accepted.append(part)
                break

    print(sum([sum(rating.values()) for rating in accepted]))  # Part 1

    # Part 2
    for name, flow in rules.items():
        conditional = []
        flow = flow.split(',')
        for i in range(len(flow) - 1):
            rule = flow[i]
            conditional.append((rule.split(':')[0][0], rule.split(':')[0][1], int(rule.split(':')[0][2:]), rule.split(':')[1]))
        rules[name] = conditional + [flow[-1]]

    # Make an XMAS tree!
    min_rating = 1
    max_rating = 4000
    start = ('in', {
        'x': (min_rating, max_rating), 'm': (min_rating, max_rating),
        'a': (min_rating, max_rating), 's': (min_rating, max_rating)
    })
    queue = [start]
    accepted_sum = 0
    while queue:
        current, intervals = queue.pop()
        if current in ('A', 'R'):
            if current == 'A':
                accepted_sum += math.prod(max_ - min_ + 1 for min_, max_ in intervals.values())
            continue

        for rating, op, boundary, next_step in rules[current][:-1]:
            min_, max_ = intervals[rating]

            # Okay, now I am lost a little
            # Why exactly do we need these two ifs?
            # if (op == '>' and boundary >= max_) or (op == '<' and boundary <= min_):
            #     continue
            #
            # if (op == '>' and boundary < min_) or (op == '<' and boundary > max_):
            #     queue.append((next_step, intervals))
            #     break

            if op == '>':
                transfer = (boundary + 1, max_)
                passthrough = (min_, boundary)
            else:
                transfer = (min_, boundary - 1)
                passthrough = (boundary, max_)
            intervals[rating] = passthrough
            intervals2 = intervals.copy()
            intervals2[rating] = transfer
            queue.append((next_step, intervals2))

        else:
            queue.append((rules[current][-1], intervals))

    print(accepted_sum)
