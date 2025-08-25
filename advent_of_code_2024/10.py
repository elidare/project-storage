dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]

with open('10.txt', 'r') as f:
    map_ = [m.strip() for m in f.readlines()]

# Let's go through the map and for each trailhead (0) try to build a trail
possible_trails = []
trail_finishes = set()
trails = 0
TRAIL_START = "0"
TRAIL_FINISH = "9"
map_m = len(map_)
map_n = len(map_[0])

for i in range(map_m):
    for j in range(map_n):
        if map_[i][j] == TRAIL_START:
            possible_trails.append((i, j, map_[i][j]))

# Aaaand this looks lika a treeeeeee
while len(possible_trails):
    x, y, point = possible_trails.pop()

    if point == TRAIL_START:
        x1, y1 = x, y

    if point == TRAIL_FINISH:
        # Completed trail, no need to search for the next step
        trail_finishes.add((x1, y1 , x, y))
        trails += 1
        continue

    for d in dirs:
        x_n, y_n = x + d[0], y + d[1]
        if x_n < 0 or x_n == map_m or y_n < 0 or y_n == map_n:
            continue

        point_n = str(int(point) + 1)
        if map_[x_n][y_n] == point_n:
            possible_trails.append((x_n, y_n, point_n))


print(len(trail_finishes))  # Part 1
print(trails)  # Part 2
