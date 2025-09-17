# I solved it myself! Just immediately thought of a system of linear equations [x * a + y * b = c]
# Of course, had to google how that thing with equations is actually called
# because I happened to forget it even in my native language
# Plus googled numpy, rounding numbers, and regexps


import numpy as np
import re


total_prizes = total_prizes_2 = 0
a_tokens = a_tokens_2 = 0
b_tokens = b_tokens_2 = 0
ADD = 10000000000000


def calculate_prize(ax, ay, bx, by, px, py):
    # a * ax + b * bx = px
    # a * ay + b * by = py
    # Coeff matrix
    matrix = np.array([[ax, bx], [ay, by]])
    equals = np.array([px, py])
    #
    # Solution
    a, b = list(np.linalg.solve(matrix, equals))
    if round(a, 2).is_integer() and 0 <= a <= 100 and round(b, 2).is_integer() and 0 <= b <= 100:
        return int(round(a, 0)) * 3, int(round(b, 0))
    return None  # not nice


def calculate_prize_billion(ax, ay, bx, by, px, py):
    # a * ax + b * bx = px
    # a * ay + b * by = py
    # Coeff matrix
    matrix = np.array([[ax, bx], [ay, by]])
    equals = np.array([px + ADD, py + ADD])
    #
    # Solution
    a, b = list(np.linalg.solve(matrix, equals))
    if round(a, 2).is_integer() and a >= 0 and round(b, 2).is_integer() and b >= 0:
        return int(round(a, 0)) * 3, int(round(b, 0))
    return None  # not nice


with open('13.txt', 'r') as f:
    # Add the last 2 \n right in text file to keep it easier
    for line in f:
        line = line.strip()
        for n in re.findall(r'X\+(\d{1,5}),\sY\+(\d{1,5})', line):
            if line.startswith('Button A'):
                ax, ay = [int(i) for i in n]
            if line.startswith('Button B'):
                bx, by = [int(i) for i in n]
        for n in re.findall(r'X=(\d{1,7}),\sY=(\d{1,7})', line):
            px, py = [int(i) for i in n]

        if not line:
            res_part_1 = calculate_prize(ax, ay, bx, by, px, py)
            if res_part_1:
                total_prizes += 1
                a_tokens += res_part_1[0]
                b_tokens += res_part_1[1]

            res_part_2 = calculate_prize_billion(ax, ay, bx, by, px, py)
            if res_part_2:
                total_prizes_2 += 1
                a_tokens_2 += res_part_2[0]
                b_tokens_2 += res_part_2[1]


print(f'Prizes: {total_prizes}, minimum tokens: {int(a_tokens + b_tokens)}')
print(f'Prizes: {total_prizes_2}, minimum tokens: {int(a_tokens_2 + b_tokens_2)}')
