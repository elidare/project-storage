#  https://www.reddit.com/r/adventofcode/comments/1hcdnk0/comment/m2fp8og/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
#  https://github.com/ArrowM/nodejs-notebook/blob/master/src/advent-of-code-2024/12/12.ts
#  https://github.com/karstendick/advent-of-code/blob/master/2024/day12/day12.py

# NOT A WORKING SOLUTION

with open('12.txt', 'r') as f:
    garden = [l.strip() for l in f.readlines()]

groups = dict()
m = len(garden)
n = len(garden[0])
total_price = 0

# for i in range(m):
#     for j in range(n):
#         current = garden[i][j]  # Current zone
#         if current not in groups:
#             # Zone current perimeter, zone current count, if there are more of the group to the east or south
#             groups[current] = [0, 0, False]
#         groups[current][1] += 1  # Add up the count
#         groups[current][2] = False  # Renew the more counter
#
#         if i - 1 < 0 or garden[i - 1][j] != current:
#             groups[current][0] += 1  # Nothing to the north or different zone, add perimeter
#         if j - 1 < 0 or garden[i][j - 1] != current:
#             groups[current][0] += 1  # Nothing to the west or different zone, add perimeter
#         if i + 1 == m or garden[i + 1][j] != current:
#             groups[current][0] += 1  # Nothing to the south or different zone, add perimeter
#         else:
#             groups[current][2] = True  # If next one is the same zone, don't calculate price
#         if j + 1 == n or garden[i][j + 1] != current:
#             groups[current][0] += 1  # Nothing to the east or different zone, add perimeter
#         else:
#             groups[current][2] = True  # If next one is the same zone, don't calculate price
#
#         if not groups[current][2]:  # If there are no more zone, calculate the price and clear the current zone
#             print(current, groups[current])
#             total_price += groups[current][0] * groups[current][1]
#             groups[current] = [0, 0, False]

# todo fix
print(total_price)
