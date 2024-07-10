from functools import cmp_to_key


def part_one():
    sum = 0

    def is_not_decoy(text, order):
        text_dict = dict()
        for t in text:
            if not t in text_dict:
                text_dict[t] = text.count(t)

        def sort_letters(letter_1, letter_2):
            if text_dict[letter_1] < text_dict[letter_2]:
                return 1
            if text_dict[letter_1] > text_dict[letter_2]:
                return -1
            if text_dict[letter_1] == text_dict[letter_2]:
                return 1 if letter_1 > letter_2 else -1

        sorted_text = ''.join(sorted(text_dict, key=cmp_to_key(sort_letters)))
        return sorted_text.startswith(order)

    with open('4.txt', 'r') as f:
        lines = [l.strip() for l in f.readlines()]

        for line in lines:
            parts = line.split('-')
            text = ''.join(parts[:-1])
            checksum, order = int(parts[-1].split('[')[0]), parts[-1].split('[')[1].replace(']', '')

            if is_not_decoy(text, order):
                sum += checksum

    return sum


def part_two():
    ALPHABET_LEN = 26

    with (open('4.txt', 'r') as f):
        lines = [l.strip() for l in f.readlines()]

        for line in lines:
            parts = line.split('-')
            text = '-'.join(parts[:-1])
            checksum = int(parts[-1].split('[')[0])
            deciphered = ''
            shift = checksum % ALPHABET_LEN

            for letter in text:
                if letter == '-':
                    deciphered += ' '
                else:
                    new_letter = chr(ord(letter) + shift) if ord(letter) + shift <= ord('z') \
                        else chr(ord(letter) + shift - ALPHABET_LEN)
                    deciphered += new_letter

            if 'north' in deciphered:
                return checksum


print(part_one())
print(part_two())
