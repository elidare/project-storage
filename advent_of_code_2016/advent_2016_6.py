# Yes, I like transposing matrices

with open('6.txt', 'r') as f:
    words = [w.strip() for w in f.readlines()]

# Transposing columns into lines to work with lines
columns = [''.join(c) for c in list(zip(*words))]


def part_one():
    correct_message = ''

    for c in columns:
        max_letter = 0
        current_letter = ''
        for letter in c:
            if letter == current_letter or c.count(letter) < max_letter:
                continue
            current_letter = letter
            max_letter = c.count(letter)
        correct_message += current_letter

    return correct_message


def part_two():
    correct_message = ''

    for c in columns:
        min_letter = len(c)
        current_letter = ''
        for letter in c:
            if letter == current_letter or c.count(letter) > min_letter:
                continue
            current_letter = letter
            min_letter = c.count(letter)
        correct_message += current_letter

    return correct_message


print(part_one())
print(part_two())
