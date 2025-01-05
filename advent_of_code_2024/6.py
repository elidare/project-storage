# I did Part 1 by myself quite easily
# And for Part 2 I read a bit of reddit for inspirations
# I did it by myself, but I kept getting the wrong answer (1 option more)
# I used this solution to get the right one https://github.com/RD-Dev-29/advent_of_code_24/blob/main/code_files/day6.py
# I figured out I had an obstacle on the starting point, and the guard perfectly started moving from there
# and ended up in a loop

import re

OBSTACLE = '#'
start_symbol = re.compile(r'(\^|>|<|v)')
directions = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}


def change_direction(current_dir):
    dirs = list(directions.keys())
    return dirs[dirs.index(current_dir) + 1 - len(dirs)]


# Part 1
def get_visited(current_position, current_direction):
    visited = list()
    while True:
        next_position = (current_position[0] + directions[current_direction][0],
                         current_position[1] + directions[current_direction][1])
        # Check next tile
        # If it is out, break
        if not (0 <= next_position[0] < map_size_v and 0 <= next_position[1] < map_size_h):
            break

        # If it is obstacle, change direction
        if map[next_position[0]][next_position[1]] == OBSTACLE:
            current_direction = change_direction(current_direction)
            continue

        # Take the next step in the current_direction
        current_position = next_position
        visited.append(current_position)

    return set(visited)


with open('6.txt', 'r') as f:
    map = [l.strip() for l in f.readlines()]

map_size_v = len(map)
map_size_h = len(map[0])

initial_position = (0, 0)  # default
initial_direction = ''  # default

for i, m in enumerate(map):
    match_obj = start_symbol.search(m)
    if match_obj:
        initial_position = i, match_obj.start()
        initial_direction = match_obj.group()


visited = get_visited(initial_position, initial_direction)
print(len(visited))  # Part 1

# Part 2
options = 0
if initial_position in visited:
    visited.remove(initial_position)  # After debugging, I figured out I need to remove the start position


def is_option(current_position, current_direction, current_obstacle):
    # Clear visited_dirs and add the first position
    visited_dirs = set()
    visited_dirs.add((*current_position, current_direction))
    # Change the map with the new obstacle
    # There was no obstacle before because we are adding obstacles on the original guard's path
    new_map = map[:]
    obstacle_row = new_map[current_obstacle[0]]
    new_map[current_obstacle[0]] = obstacle_row[:current_obstacle[1]] + OBSTACLE + obstacle_row[current_obstacle[1] + 1:]

    while True:
        next_position = (current_position[0] + directions[current_direction][0],
                         current_position[1] + directions[current_direction][1])

        # Check next tile
        # If it is out, it is not the option
        if not (0 <= next_position[0] < map_size_v and 0 <= next_position[1] < map_size_h):
            return False

        # If it is obstacle, change direction
        if new_map[next_position[0]][next_position[1]] == OBSTACLE:
            current_direction = change_direction(current_direction)
            continue

        # Check if the next step has already been in visited
        # Meaning we are in the loop
        if (*next_position, current_direction) in visited_dirs:
            return True

        # Take the next step in the current_direction
        current_position = next_position
        visited_dirs.add((*current_position, current_direction))


for p in visited:
    if is_option(initial_position, initial_direction, p):
        options += 1

print(options)  # Part 2
