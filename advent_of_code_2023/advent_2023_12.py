# DISCLAIMER
# Uses the following reddit solution
# https://www.reddit.com/r/adventofcode/comments/18ge41g/comment/kd0oj1t/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
# I took it and errrm UN-DER-STOOD..... kinda
from functools import cache

with open('12.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]
    springs_input = []
    for line in lines:
        springs, numbers = line.split()[0], line.split()[1]
        springs_input.append([springs, tuple(int(n) for n in numbers.split(','))])

    @cache  # too slow without the cache - stpres function values
    def numlegal(springs, count):
        springs = springs.lstrip('.')  # ignore leading dots

        # ['', ()] is legal
        if springs == '':
            return int(count == ())

        # [s, ()] is legal so long as s has no '#' (we can convert '?' to '.')
        if count == ():
            return int(springs.find('#') == -1)

        # s starts with '#' so remove the first spring
        if springs[0] == '#':
            if len(springs) < count[0] or '.' in springs[:count[0]]:
                return 0  # impossible - not enough space for the spring
            elif len(springs) == count[0]:
                return int(len(count) == 1)  # single spring, right size
            elif springs[count[0]] == '#':
                return 0  # springs must be separated by '.' (or '?')
            else:
                return numlegal(springs[count[0] + 1:], count[1:])  # one less spring

        # numlegal springs if we convert the first '?' to '#' + '.'
        return numlegal('#' + springs[1:], count) + numlegal(springs[1:], count)

    # Part 1
    print(sum(numlegal(springs, count) for [springs, count] in springs_input))

    # Part 2
    springs_input_2 = [[(spring_row[0] + '?') * 4 + spring_row[0], spring_row[1] * 5] for spring_row in springs_input]
    print(sum(numlegal(springs, count) for [springs, count] in springs_input_2))
