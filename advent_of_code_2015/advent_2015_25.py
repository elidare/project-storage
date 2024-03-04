def part_one():
    # Do not commit your puzzle input
    code_row = 6
    code_col = 6
    number = 20151125  # Position 1:1

    # I'll skip the position 1:1 (counter 1 + 1 = 2),
    # and move to the next diagonal 2:1 and 1:2 (counter 2 + 1 = 3) etc
    row_col_diagonal = 3

    while True:
        for row in range(row_col_diagonal - 1, 0, -1):
            col = row_col_diagonal - row

            # Calculate number
            number = (number * 252533) % 33554393

            if row == code_row and col == code_col:
                return number

        row_col_diagonal += 1


print(part_one())
