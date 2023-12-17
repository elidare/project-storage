import sys

sys.setrecursionlimit(10000)
# I solved it only by recursion, and I am pretty lazy to make it neat
# I got into 1000 limit of calls as in maximum recursion depth, so I am hacking it a little to make it work
# Otherwise I would have done something like a calling stack with tiles to go next
# e.g. while True: append to tile stack [(0, 0, RIGHT)], go next once, and if I got into splitting tile,
# then tile stack > append (second direction after split) to be operated after the first go_next calling returns None
# The used tile from tile stack is popped, and when the tile stack length == 0, break the while block

with open('16.txt', 'r') as f:
    contraption = [list(line.strip()) for line in f.readlines()]
    RIGHT = 'right'
    LEFT = 'left'
    UP = 'up'
    DOWN = 'down'
    energised = dict()

    def go_next(i, j, direction):
        if i < 0 or j < 0 or i >= len(contraption) or j >= len(contraption[0]):
            # End of field
            return
        if (i, j) in energised:
            if direction in energised[(i, j)]:
                return
            energised[(i, j)].append(direction)
        else:
            energised[(i, j)] = [direction]

        if contraption[i][j] == '.':
            i = i + 1 if direction == DOWN else i - 1 if direction == UP else i
            j = j + 1 if direction == RIGHT else j - 1 if direction == LEFT else j
            go_next(i, j, direction)
        elif contraption[i][j] == '|':
            if direction in (UP, DOWN):
                i = i + 1 if direction == DOWN else i - 1
                go_next(i, j, direction)
            else:
                go_next(i + 1, j, DOWN)
                go_next(i - 1, j, UP)
        elif contraption[i][j] == '-':
            if direction in (LEFT, RIGHT):
                j = j + 1 if direction == RIGHT else j - 1
                go_next(i, j, direction)
            else:
                go_next(i, j + 1, RIGHT)
                go_next(i, j - 1, LEFT)
        elif contraption[i][j] == '/':
            if direction in (LEFT, RIGHT):
                i = i + 1 if direction == LEFT else i - 1
                go_next(i, j, DOWN if direction == LEFT else UP)
            else:
                j = j + 1 if direction == UP else j - 1
                go_next(i, j, RIGHT if direction == UP else LEFT)
        elif contraption[i][j] == '\\':
            if direction in (LEFT, RIGHT):
                i = i + 1 if direction == RIGHT else i - 1
                go_next(i, j, DOWN if direction == RIGHT else UP)
            else:
                j = j + 1 if direction == DOWN else j - 1
                go_next(i, j, RIGHT if direction == DOWN else LEFT)

    # Part 1
    # go_next(0, 0, RIGHT)
    # print(len(energised.keys()))  # How many energised?

    # Part 2
    # Let's go through all the edges and count the energised ones
    max_energised = 0
    for m in range(len(contraption)):
        for n in range(len(contraption[m])):
            if m == 0:
                energised = dict()
                go_next(m, n, DOWN)
                if len(energised.keys()) > max_energised:
                    max_energised = len(energised.keys())
            if n == 0:
                energised = dict()
                go_next(m, n, RIGHT)
                if len(energised.keys()) > max_energised:
                    max_energised = len(energised.keys())
            if m == len(contraption) - 1:
                energised = dict()
                go_next(m, n, UP)
                if len(energised.keys()) > max_energised:
                    max_energised = len(energised.keys())
            if n == len(contraption[m]) - 1:
                energised = dict()
                go_next(m, n, LEFT)
                if len(energised.keys()) > max_energised:
                    max_energised = len(energised.keys())

    print(max_energised)
