def part_one():
    start_position = (0, 0)  # x, y
    current_position = start_position  # x, y
    current_direction_index = 0
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # North, East, South, West

    with open('1.txt', 'r') as f:
        instructions = [i.strip() for i in f.readline().split(',')]

        for i in instructions:
            turn, steps = i[0:1], int(i[1:])
            if turn == 'R':
                current_direction_index = current_direction_index + 1 if current_direction_index + 1 < len(directions) else 0
            else:
                current_direction_index = current_direction_index - 1 if current_direction_index - 1 >= 0 else len(directions) - 1

            new_direction = directions[current_direction_index]
            current_position = (current_position[0] + steps * new_direction[0],
                                current_position[1] + steps * new_direction[1])

        return abs(current_position[0] - start_position[0]) + abs(current_position[1] - start_position[1])


def part_two():
    start_position = (0, 0)  # x, y
    current_position = start_position  # x, y
    current_direction_index = 0
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # North, East, South, West
    locations = list()  # I decided just to store the visited location in a list and to search through it on every step

    with (open('1.txt', 'r') as f):
        instructions = [i.strip() for i in f.readline().split(',')]

        for i in instructions:
            turn, steps = i[0:1], int(i[1:])
            if turn == 'R':
                current_direction_index = current_direction_index + 1 if current_direction_index + 1 < len(directions) else 0
            else:
                current_direction_index = current_direction_index - 1 if current_direction_index - 1 >= 0 \
                    else len(directions) - 1

            new_direction = directions[current_direction_index]

            for _ in range(1, steps + 1):
                current_position = (current_position[0] + new_direction[0],
                                    current_position[1] + new_direction[1])
                if current_position in locations:
                    return abs(current_position[0] - start_position[0]) + abs(current_position[1] - start_position[1])
                else:
                    locations.append(current_position)


print(part_one())  # Shortest path
print(part_two())  # Shortest path to a location we visit twice
