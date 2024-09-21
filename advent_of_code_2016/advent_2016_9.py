# Disclaimer
# Part 1 is done by me, but it is so VERY NOT optimised for Part 2
# For Part 2, I had a look on Reddit for some ideas and was impressed by this algorithm
# https://www.reddit.com/r/adventofcode/comments/5hbygy/comment/dazentu/ by @rhardih
# https://github.com/rhardih/aoc/blob/master/2016/9p2.c

OPENING = '('
CLOSING = ')'
MULTIPLY = 'x'


def decompress(line):
    new_line = ''
    index = 0
    opened = False
    current_rule = ''

    while index < len(line):
        if line[index] == OPENING:
            opened = True
            index += 1
            continue

        if not opened:
            next_opening = line.find(OPENING, index + 1)
            if next_opening == -1:
                new_line += line[index:]
                break
            new_line += line[index:next_opening]
            index = next_opening
            continue

        if line[index] != CLOSING:
            next_closing = line.find(CLOSING, index)
            current_rule = line[index:next_closing]
            index = next_closing
            continue

        length, repeat = [int(i) for i in current_rule.split(MULTIPLY)]
        new_line += line[index + 1:index + length + 1] * repeat
        opened = False
        current_rule = ''
        index += length + 1

    return new_line


def decompress_by_math(line):
    # Uses https://github.com/rhardih/aoc/blob/master/2016/9p2.c algorithm
    weights = [1] * len(line)
    opened = False
    current_rule = ''
    decompressed_len = 0

    for i in range(len(line)):
        if line[i] == OPENING:
            opened = True
            continue
        if opened and line[i] != CLOSING:
            current_rule += line[i]
            continue
        if line[i] == CLOSING:
            length, repeat = [int(j) for j in current_rule.split(MULTIPLY)]
            for k in range(length):
                index = i + k + 1
                weights[index] = weights[index] * repeat
            opened = False
            current_rule = ''
            continue

        decompressed_len += weights[i]

    return decompressed_len


with open('9.txt', 'r') as f:
    line = f.readline().strip()

    # Part 1
    decompressed = len(decompress(line))
    print(decompressed)

    # Part 2
    print(decompress_by_math(line))
