# DISCLAIMER
# I give up, I just give up
# I am a non-coding QA, come on!
# This solution is a copy of
# https://www.reddit.com/r/adventofcode/comments/18k9ne5/comment/kdsrq6g/?utm_source=share&utm_medium=web2x&context=3
# https://github.com/mgtezak/Advent_of_Code/blob/master/2023/Day_17.py
# Also I haven't thought of storing directions as dx, dy, but it seems quite reasonable!

from heapq import heappop, heappush


with open('17.txt', 'r') as f:
    heat_loss_map = [[int(n) for n in line.strip()] for line in f.readlines()]
    directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    visited = set()
    queue = [(0, 0, 0, 0, 0, 0)]  # heat_loss, x, y, current_run, dx, dy

    # Part 1
    while queue:
        heat_loss, x, y, current_run, dx, dy = heappop(queue)

        if x == len(heat_loss_map) - 1 and y == len(heat_loss_map[0]) - 1:
            break

        if any((x, y, k_, dx, dy) in visited for k_ in range(1, current_run + 1)):
            continue

        visited.add((x, y, current_run, dx, dy))

        for new_dx, new_dy in directions:
            straight = (new_dx == dx and new_dy == dy)
            new_x, new_y = x + new_dx, y + new_dy

            if (new_dx == -dx and new_dy == -dy) or (current_run == 3 and straight) or \
                    new_x < 0 or new_y < 0 or new_x == len(heat_loss_map) or new_y == len(heat_loss_map[0]):
                continue

            new_run = current_run + 1 if straight else 1
            heappush(queue, (heat_loss + heat_loss_map[new_x][new_y], new_x, new_y, new_run, new_dx, new_dy))

    print(heat_loss)  # Part 1 answer

    # Part 2
    visited = set()
    queue = [(0, 0, 0, 0, 0, 1), (0, 0, 0, 0, 1, 0)]  # heat_loss, x, y, current_run, dx, dy
    while queue:
        heat_loss, x, y, current_run, dx, dy = heappop(queue)

        if x == len(heat_loss_map) - 1 and y == len(heat_loss_map[0]) - 1:
            if current_run < 4:
                continue
            break

        if (x, y, current_run, dx, dy) in visited:
            continue

        visited.add((x, y, current_run, dx, dy))

        for new_dx, new_dy in directions:
            straight = (new_dx == dx and new_dy == dy)
            new_x, new_y = x + new_dx, y + new_dy

            # But I don't really get how the requirement of 4 tiles before the end is fulfilled
            if (new_dx == -dx and new_dy == -dy) or (current_run == 10 and straight) or \
                    (current_run < 4 and not straight) or \
                    new_x < 0 or new_y < 0 or new_x == len(heat_loss_map) or new_y == len(heat_loss_map[0]):
                continue

            new_run = current_run + 1 if straight else 1
            heappush(queue, (heat_loss + heat_loss_map[new_x][new_y], new_x, new_y, new_run, new_dx, new_dy))

    print(heat_loss)  # Part 2 answer
