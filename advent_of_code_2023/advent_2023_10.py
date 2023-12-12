with open('10.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

    class Directions:
        DIRECTION_WEST = 'west'
        DIRECTION_EAST = 'east'
        DIRECTION_NORTH = 'north'
        DIRECTION_SOUTH = 'south'

    tiles = {
        '|': [Directions.DIRECTION_NORTH, Directions.DIRECTION_SOUTH], '-': [Directions.DIRECTION_WEST, Directions.DIRECTION_EAST],
        'L': [Directions.DIRECTION_NORTH, Directions.DIRECTION_EAST], 'J': [Directions.DIRECTION_NORTH, Directions.DIRECTION_WEST],
        '7': [Directions.DIRECTION_SOUTH, Directions.DIRECTION_WEST], 'F': [Directions.DIRECTION_SOUTH, Directions.DIRECTION_EAST]
    }
    directions_opposite = {
        Directions.DIRECTION_NORTH: Directions.DIRECTION_SOUTH,
        Directions.DIRECTION_SOUTH: Directions.DIRECTION_NORTH,
        Directions.DIRECTION_WEST: Directions.DIRECTION_EAST,
        Directions.DIRECTION_EAST: Directions.DIRECTION_WEST
    }

    s_tile = None
    maze = []
    for i in range(len(lines)):
        if 'S' in lines[i]:
            s_tile = (i, lines[i].find('S'))
        maze.append([tile for tile in lines[i]])

    def get_next_direction(tile, direction):
        return [d for d in tiles[tile] if d != directions_opposite[direction]][0]

    def is_attached(tile, direction):
        return any([direction == directions_opposite[d] for d in tiles[tile]])

    def get_next_tile(i, j, direction):
        if direction == Directions.DIRECTION_NORTH and i - 1 >= 0 and maze[i - 1][j] in tiles and \
                is_attached(maze[i - 1][j], Directions.DIRECTION_NORTH):
            return i - 1, j, get_next_direction(maze[i - 1][j], Directions.DIRECTION_NORTH)
        if direction == Directions.DIRECTION_EAST and j + 1 < len(maze[i]) and maze[i][j + 1] in tiles and \
                is_attached(maze[i][j + 1], Directions.DIRECTION_EAST):
            return i, j + 1, get_next_direction(maze[i][j + 1], Directions.DIRECTION_EAST)
        if direction == Directions.DIRECTION_SOUTH and i + 1 < len(maze) and maze[i + 1][j] in tiles and \
                is_attached(maze[i + 1][j], Directions.DIRECTION_SOUTH):
            return i + 1, j, get_next_direction(maze[i + 1][j], Directions.DIRECTION_SOUTH)
        if direction == Directions.DIRECTION_WEST and j - 1 >= 0 and maze[i][j - 1] in tiles and \
                is_attached(maze[i][j - 1], Directions.DIRECTION_WEST):
            return i, j - 1, get_next_direction(maze[i][j - 1], Directions.DIRECTION_WEST)
        return None

    def get_s_replacement():
        i, j = s_tile[0], s_tile[1]
        if i - 1 >= 0 and maze[i - 1][j] in ('7', '|', 'F'):
            if j + 1 < len(maze[i]) and maze[i][j + 1] in ('-', 'J', '7'):
                return 'L'
            if i + 1 < len(maze) and maze[i + 1][j] in ('|', 'J', 'L'):
                return '|'
            if j - 1 >= 0 and maze[i][j - 1] in ('-', 'L', 'F'):
                return 'J'
        if j + 1 < len(maze[i]) and maze[i][j + 1] in ('-', 'J', '7'):
            if i + 1 < len(maze) and maze[i + 1][j] in ('|', 'J', 'L'):
                return 'F'
            if j - 1 >= 0 and maze[i][j - 1] in ('-', 'L', 'F'):
                return '-'
        return '7'


    # Part 1 - Initial solution
    # Should be only 2 directions
    possible_next_tiles = list(filter(lambda x: x, [
        get_next_tile(s_tile[0], s_tile[1], Directions.DIRECTION_NORTH),
        get_next_tile(s_tile[0], s_tile[1], Directions.DIRECTION_EAST),
        get_next_tile(s_tile[0], s_tile[1], Directions.DIRECTION_SOUTH),
        get_next_tile(s_tile[0], s_tile[1], Directions.DIRECTION_WEST),
    ]))

    path_1 = [s_tile]
    path_2 = [s_tile]
    path_1.append(possible_next_tiles[0])
    path_2.append(possible_next_tiles[1])

    while True:
        current_tile = path_1[-1]
        path_1.append(get_next_tile(current_tile[0], current_tile[1], current_tile[2]))

        current_tile = path_2[-1]
        path_2.append(get_next_tile(current_tile[0], current_tile[1], current_tile[2]))

        if (path_1[-1][0], path_1[-1][1]) == (path_2[-1][0], path_2[-1][1]):
            break

    print(len(path_1) - 1)  # Farthest point

    # Part 1 rewritten - Thank you reddit
    loop = [s_tile]
    loop.append(possible_next_tiles[0])
    while True:
        current_tile = loop[-1]
        last = loop.pop()
        loop.append((last[0], last[1]))  # Messy, but I don't want to keep direction in the loop
        next_tile = get_next_tile(current_tile[0], current_tile[1], current_tile[2])
        if next_tile:
            loop.append(get_next_tile(current_tile[0], current_tile[1], current_tile[2]))
        else:  # We found S
            break

    print(int(len(loop) / 2))  # Farthest point

    # Part 2
    # Thank you reddit https://www.reddit.com/r/adventofcode/comments/18eza5g/2023_day_10_animated_visualization/
    # I'll replace S with an appropriate tile
    maze[s_tile[0]][s_tile[1]] = get_s_replacement()

    result = 0
    for i in range(len(maze)):
        opened = False
        for j in range(len(maze[i])):
            current_tile = maze[i][j]
            if current_tile in ('|', '7', 'F') and (i, j) in loop:
                opened = not opened
            if opened and (i, j) not in loop:
                result += 1

    print(result)
