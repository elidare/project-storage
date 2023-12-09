with open('3.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]
    numbers = []
    numbers_gears = []

    # Part 1
    def is_symbol(symbol):
        return symbol != '.'

    def write_number(number, has_adjacent):
        if number and has_adjacent:
            numbers.append(int(number))
        return '', False

    # Part 2
    def is_gear(symbol):
        return symbol == '*'

    def find_number(line, number, j):
        number_result = number
        start_index = j

        for n in range(j - 1, -1, -1):
            if line[n].isdigit():
                number_result = line[n] + number_result
                start_index = n
            else:
                break

        for o in range(j + 1, len(line)):
            if line[o].isdigit():
                number_result += line[o]
            else:
                break

        return number_result, start_index

    for i in range(0, len(lines)):
        number = ''
        has_adjacent = False
        for j in range(0, len(lines[i])):
            # Part 1
            if lines[i][j].isdigit():
                number += lines[i][j]

                if not has_adjacent:  # Check previous column
                    has_adjacent = j > 0 and (is_symbol(lines[i][j - 1]) and (not lines[i][j - 1].isdigit()) or
                                              i > 0 and is_symbol(lines[i - 1][j - 1]) or
                                              i < len(lines) - 1 and is_symbol(lines[i + 1][j - 1]))

                if not has_adjacent:  # Check the same column
                    has_adjacent = i > 0 and is_symbol(lines[i - 1][j]) or \
                                   i < len(lines) - 1 and is_symbol(lines[i + 1][j])

                if not has_adjacent:  # Check the next column
                    has_adjacent = j < len(lines[i]) - 1 and \
                                   (is_symbol(lines[i][j + 1]) and (not lines[i][j + 1].isdigit()) or
                                    i > 0 and is_symbol(lines[i - 1][j + 1]) or
                                    i < len(lines) - 1 and is_symbol(lines[i + 1][j + 1]))

                if j == len(lines[i]) - 1:
                    number, has_adjacent = write_number(number, has_adjacent)
            else:
                number, has_adjacent = write_number(number, has_adjacent)

            # Part 2
            if is_gear(lines[i][j]):
                numbers_around = set()  # Set to exclude finding the same number at the same position twice
                for k in [-1, 0, 1]:
                    for m in [-1, 0, 1]:
                        if lines[i + k][j + m].isdigit():
                            # Probably need try-catch for Out of range Error
                            numbers_around.add(find_number(lines[i + k], lines[i + k][j + m], j + m))
                if len(numbers_around) == 2:
                    numbers_around = list(numbers_around)
                    numbers_gears.append(int(numbers_around[0][0]) * int(numbers_around[1][0]))

    # print(sum(numbers))
    print(sum(numbers_gears))

