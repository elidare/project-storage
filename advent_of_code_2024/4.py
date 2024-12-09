import time


XMAS = 'XMAS'
total = 0

with open('4.txt', 'r') as f:
    layout = [l.strip() for l in f.readlines()]

start_1 = time.time()
layout_backwards = list()  # For the diagonal down let's just have the list of lines backwards
size_v = len(layout)
size_h = len(layout[0])

# The idea here is to count how many times "XMAS" appears in every horizontal, vertical, and diagonal line
for l in layout:
    total += l.count(XMAS)
    total += l[::-1].count(XMAS)
    layout_backwards.append(l[::-1])

layout_vert = [''.join(r) for r in list(zip(*layout))]  # Transposing

for l in layout_vert:
    total += l.count(XMAS)
    total += l[::-1].count(XMAS)

layout_diag_up = list()
layout_diag_down = list()
for i in range(size_v + size_h - 1):
    l_diag_up = ''
    l_diag_down = ''
    for j in range(i + 1):
        if j < 0 or j >= size_v:
            continue
        if i - j < 0 or i - j >= size_h:
            continue
        l_diag_up += layout[j][i - j]
        l_diag_down += layout_backwards[j][i - j]
    layout_diag_up.append(l_diag_up)
    layout_diag_down.append(l_diag_down)

for l in layout_diag_up:
    total += l.count(XMAS)
    total += l[::-1].count(XMAS)

for l in layout_diag_down:
    total += l.count(XMAS)
    total += l[::-1].count(XMAS)

print(total)
end_1 = time.time()
print(end_1 - start_1)  # 0.006-0.008

# Part 1 another way that actually takes longer
start_2 = time.time()
layout_arr = [list(l) for l in layout]
total_new = 0

for i in range(size_v):
    for j in range(size_h):
        if layout_arr[i][j] != XMAS[0]:
            continue
        # Let's find XMAS by going to every direction and checking if it has next M-A-S
        for s in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]:
            for k in range(1, len(XMAS)):
                current = i + s[0] * k, j + s[1] * k
                if current[0] < 0 or current[0] >= size_v:
                    break
                if current[1] < 0 or current[1] >= size_h:
                    break
                if layout_arr[current[0]][current[1]] != XMAS[k]:
                    break
            else:
                total_new += 1

print(total_new)
end_2 = time.time()
print(end_2 - start_2)  # 0.017-0.018

# Part 2:
# There can be only following combinations:
# M.M   M.S   S.M   S.S
# .A.   .A.   .A.   .A.
# S.S   M.S   S.M   M.M
# So we'll have one go through the array, and if A is found
# check that [(-1,-1), (-1,1), (1,1), (1,-1)] are MMSS, MSSM, SMMS, or SSMM
total_part_2 = 0

for i in range(size_v):
    for j in range(size_h):
        if layout_arr[i][j] != XMAS[2]:  # A-letter
            continue
        surrounding = ''
        for s in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:
            current = i + s[0], j + s[1]
            if current[0] < 0 or current[0] >= size_v:
                break
            if current[1] < 0 or current[1] >= size_h:
                break
            surrounding += layout_arr[current[0]][current[1]]
        if surrounding in ["MMSS", "MSSM", "SMMS", "SSMM"]:
            total_part_2 += 1

print(total_part_2)
