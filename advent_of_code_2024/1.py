left = []
right = []

with open('1.txt', 'r') as f:
    while True:
        line = f.readline().strip()

        if not line:
            break
        left_id, right_id = [int(i) for i in line.split()]

        left.append(left_id)
        right.append(right_id)

left = sorted(left)
right = sorted(right)

# Part 1
total_distance = sum([abs(p[1] - p[0]) for p in zip(left, right)])
print(total_distance)

# Part 2
similarity_score = 0
for j in left:
    similarity_score += j * right.count(j)

print(similarity_score)
