directions = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}


def part_one():
    numpad = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    min_pad, max_pad = 0, len(numpad)
    current_button = (1, 1)  # 5 is located at 1, 1

    with open('2.txt', 'r') as f:
        instructions = [l.strip() for l in f.readlines()]
        code = ''

        for inst in instructions:
            for d in inst:
                current_direction = directions[d]
                new_x, new_y = current_button[0] + current_direction[0], current_button[1] + current_direction[1]
                if not (min_pad <= new_x < max_pad and min_pad <= new_y < max_pad):
                    continue
                current_button = (new_x, new_y)

            code += str(numpad[current_button[0]][current_button[1]])

    return code


def part_two():
    # I'll put X at the edges
    numpad = [['X', 'X', '1', 'X', 'X'],
              ['X', '2', '3', '4', 'X'],
              ['5', '6', '7', '8', '9'],
              ['X', 'A', 'B', 'C', 'X'],
              ['X', 'X', 'D', 'X', 'X']]
    min_pad, max_pad = 0, len(numpad)
    current_button = (2, 0)  # 5 is located at 2, 0

    with open('2.txt', 'r') as f:
        instructions = [l.strip() for l in f.readlines()]
        code = ''

        for inst in instructions:
            for d in inst:
                current_direction = directions[d]
                new_x, new_y = current_button[0] + current_direction[0], current_button[1] + current_direction[1]

                if min_pad <= new_x < max_pad and min_pad <= new_y < max_pad and numpad[new_x][new_y] != 'X':
                    current_button = (new_x, new_y)
                else:
                    # If the next tile is over the edge, or equals X, - skip it
                    continue

            code += str(numpad[current_button[0]][current_button[1]])

    return code


print(part_one())
print(part_two())
