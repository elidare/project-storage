SCREEN_WIDTH = 7
SCREEN_HEIGHT = 3
ON = '#'
OFF = '.'

# I think I should do a class with a screen and methods rect and rotate, but let's just go with global var 'screen'
screen = [OFF * SCREEN_WIDTH] * SCREEN_HEIGHT


def rect(m, n):
    if m > SCREEN_WIDTH or n > SCREEN_HEIGHT:
        return
    for i in range(n):
        screen[i] = ON * m + screen[i][m:]


def rotate_row(row_number, by):
    if row_number >= SCREEN_HEIGHT:
        return
    if by >= SCREEN_WIDTH:
        by = by - SCREEN_WIDTH

    # I know, that BY is always >= 0 by the input analysis
    screen[row_number] = screen[row_number][SCREEN_WIDTH - by:] + screen[row_number][:SCREEN_WIDTH - by]


def rotate_column(column_number, by):
    if column_number >= SCREEN_WIDTH:
        return
    if by >= SCREEN_HEIGHT:
        by = by - SCREEN_HEIGHT

    # I know, that BY is always >= 0 by the input analysis
    column = ''.join([r[column_number] for r in screen])
    new_column = column[SCREEN_HEIGHT - by:] + column[:SCREEN_HEIGHT - by]
    for i in range(SCREEN_HEIGHT):
        screen[i] = screen[i][:column_number] + new_column[i] + screen[i][column_number + 1:]


with open('8.txt', 'r') as f:
    count_on = 0

    while True:
        line = f.readline().strip()

        if not line:
            break

        if line.startswith('rect'):
            m, n = [int(num) for num in line.split()[1].split('x')]
            rect(m, n)
        elif line.startswith('rotate column'):
            column_number, by = [int(num.strip()) for num in line.split('=')[1].split('by')]
            rotate_column(column_number, by)
        elif line.startswith('rotate row'):
            row_number, by = [int(num.strip()) for num in line.split('=')[1].split('by')]
            rotate_row(row_number, by)

    for row in screen:
        print(row)  # Let's see, what is on the screen! Goes for Part 2
        count_on += row.count(ON)

    print(count_on)  # Part 1
