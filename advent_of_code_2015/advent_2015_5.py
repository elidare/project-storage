with open('5.txt', 'r') as f:
    strings = [s.strip() for s in f.readlines()]


def part_one():
    count_nice = 0

    def is_nice(string):
        has_doubles = False
        # Has at least 3 vowels
        has_sufficient_vowels = sum(map(string.count, list('aeiou'))) >= 3
        # Find double letters
        for i in range(len(string) - 1):
            if string[i] == string[i + 1]:
                has_doubles = True
                break
        # Check if there are restricted strings
        restricted = sum(map(string.count, ['ab', 'cd', 'pq', 'xy']))
        return has_sufficient_vowels and has_doubles and not restricted

    for string in strings:
        if is_nice(string):
            count_nice += 1

    return count_nice


def part_two():
    count_nice = 0

    def is_nice(string):
        has_doubles = False
        contains_pair = False
        # Contains a pair of letters twice
        for i in range(0, len(string) - 1):
            pair = string[i] + string[i + 1]
            if string.find(pair, i + 2) > -1:
                contains_pair = True
                break

        # Contains at least one letter at the position i + 2
        for i in range(len(string) - 2):
            if string[i] == string[i + 2]:
                has_doubles = True
                break
        return contains_pair and has_doubles

    for string in strings:
        if is_nice(string):
            count_nice += 1

    return count_nice


print(part_one())
print(part_two())
