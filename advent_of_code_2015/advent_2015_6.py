with open('6.txt', 'r') as f:
    rules = [s.strip() for s in f.readlines()]
    TURN_ON = 'turn on'
    TURN_OFF = 'turn off'
    TOGGLE = 'toggle'
    SIZE = 1000


def part_one():
    lights_grid = [[False] * SIZE for _ in range(SIZE)]

    def get_command(rule):
        command = TURN_ON if rule.startswith(TURN_ON) else TURN_OFF if rule.startswith(TURN_OFF) else TOGGLE
        coord_start, coord_end = [c.strip() for c in rule[len(command) + 1:].split('through')]
        return command, tuple(int(i) for i in coord_start.split(',')), tuple(int(i) for i in coord_end.split(','))

    for rule in rules:
        command, coord_start, coord_end = get_command(rule)

        for i in range(coord_start[0], coord_end[0] + 1):
            for j in range(coord_start[1], coord_end[1] + 1):
                if command == TOGGLE:
                    lights_grid[i][j] = not lights_grid[i][j]
                else:
                    lights_grid[i][j] = command == TURN_ON

    return sum([sum(lights_grid[m]) for m in range(len(lights_grid))])


def part_two():
    lights_grid = [[0] * SIZE for _ in range(SIZE)]

    def get_command(rule):
        command = TURN_ON if rule.startswith(TURN_ON) else TURN_OFF if rule.startswith(TURN_OFF) else TOGGLE
        coord_start, coord_end = [c.strip() for c in rule[len(command) + 1:].split('through')]
        return command, tuple(int(i) for i in coord_start.split(',')), tuple(int(i) for i in coord_end.split(','))

    for rule in rules:
        command, coord_start, coord_end = get_command(rule)

        for i in range(coord_start[0], coord_end[0] + 1):
            for j in range(coord_start[1], coord_end[1] + 1):
                if command == TOGGLE:
                    lights_grid[i][j] += 2
                elif command == TURN_ON:
                    lights_grid[i][j] += 1
                else:
                    lights_grid[i][j] = lights_grid[i][j] - 1 if lights_grid[i][j] > 0 else 0

    return sum([sum(lights_grid[m]) for m in range(len(lights_grid))])


# print(part_one())
print(part_two())
