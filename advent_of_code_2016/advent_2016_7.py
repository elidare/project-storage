# For this one I'll try to read the file line by line
import re


tls_count = 0
ssl_count = 0
ABBA_LEN = 4
ABA_LEN = 3


def split_line(line):
    # I googled this RE and list handling
    return re.findall(r'\[(.*?)\]', line), list(s.split(']')[-1] for s in line.split('['))


def is_tls(line):
    def is_abba(text):
        if len(text) < ABBA_LEN:
            return False
        for i in range(len(text) - ABBA_LEN + 1):
            if text[i] != text[i + 1] and text[i:i + 2] == text[i + 3:i + 1:-1]:
                return True
        return False

    brackets_texts, non_brackets_texts = split_line(line)

    for text in brackets_texts:
        if is_abba(text):
            return False
    for text in non_brackets_texts:
        if is_abba(text) or is_abba(text):
            return True
    return False


def is_ssl(line):
    brackets_texts, non_brackets_texts = split_line(line)

    for n_b_text in non_brackets_texts:
        for i in range(len(n_b_text) - ABA_LEN + 1):
            if n_b_text[i] != n_b_text[i + 1] and n_b_text[i] == n_b_text[i + 2]:
                seq = n_b_text[i:i + 3]
                # Search in the brackets at once
                for b_text in brackets_texts:
                    if seq[1] + seq[0] + seq[1] in b_text:
                        return True

    return False


with open('7.txt', 'r') as f:
    while True:
        line = f.readline().strip()

        if not line:
            break

        if is_tls(line):
            tls_count += 1

        if is_ssl(line):
            ssl_count += 1


print(tls_count)
print(ssl_count)
