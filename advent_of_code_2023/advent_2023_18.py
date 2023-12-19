with open('18.txt', 'r') as f:
    digging_map = [line.strip().split() for line in f.readlines()]
    ground = []
    holes = dict()
    directions = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}
    # For Part 1 I've just thought to try to copy-paste the Day 10 solution because I can
    # So I'll make the grid of F---J and count the insides
    # ....... And after I'm done with shoelace formula, I see how much effort I could have saved...
    corners = {
        'RD': '7', 'RU': 'J',
        'LD': 'F', 'LU': 'L',
        'UL': '7', 'UR': 'F',
        'DL': 'J', 'DR': 'L',
        'R': '-', 'L': '-',
        'U': '|', 'D': '|'
    }

    previous_direction = ''
    loop_direction = ''
    for direction, run, hex_data in digging_map:
        if not loop_direction:
            loop_direction = direction
        if previous_direction:
            holes[(last_tile[0] + dx, last_tile[1] + dy)] = corners[previous_direction + direction]
        for i in range(int(run)):
            holes_tiles = list(holes.keys())
            last_tile = (0, 0) if len(holes_tiles) == 0 else holes_tiles[-1]
            dx, dy = directions[direction]
            if i == int(run) - 1:
                previous_direction = direction
            else:
                holes[(last_tile[0] + dx, last_tile[1] + dy)] = corners[direction]

    # Add the starting tile
    holes[(holes_tiles[-1][0] + dx, holes_tiles[-1][1] + dy)] = corners[direction + loop_direction]

    row_index = 0
    min_col = max_col = 0
    holes_tiles = sorted(holes.keys())
    while True:
        row = list(map(lambda tile: tile[1], filter(lambda tile: tile[0] == row_index, holes_tiles)))
        if len(row) == 0:
            break

        min_col = min(row) if min(row) < min_col else min_col
        max_col = max(row) if max(row) > max_col else max_col
        row_index += 1

    min_row, max_row = holes_tiles[0][0], holes_tiles[-1][0]
    diff_col, diff_row = 0 - min_col, 0 - min_row
    m, n = max_row - min_row + 1, max_col - min_col + 1
    inside_size = 0
    for i in range(m):
        ground.append([])
        opened = False
        for j in range(n):
            if (i - diff_row, j - diff_col) in holes_tiles:
                tile = holes[(i - diff_row, j - diff_col)]
            else:
                tile = '.'

            # And here goes Day 10 solution
            if tile in ('|', '7', 'F', 'S'):
                opened = not opened
            if opened and (i - diff_row, j - diff_col) not in holes_tiles:
                tile = '+'
                inside_size += 1

            ground[i].append(tile)

        # print(''.join(ground[i]))  # This is to make it look nice as a map

    # Part 1
    print(inside_size + len(holes_tiles))

    # Part 2
    def exract_data(hex_data):
        r = int(hex_data[2:7], 16)
        d = ['R', 'D', 'L', 'U'][int(hex_data[7])]
        return r, d

    holes_bigger = list()
    perimeter = 0
    x = y = 0
    for r, d, hex_data in digging_map:
        run, direction = exract_data(hex_data)
        dx, dy = directions[direction]
        x = x + dx * run if direction in ('U', 'D') else x
        y = y + dy * run if direction in ('L', 'R') else y
        perimeter += run
        holes_bigger.append((x, y))

    # Science, b**ch!
    # Shoelace formula, thank you reddit
    size_bigger = 0
    for i in range(len(holes_bigger) - 1):
        size_bigger += holes_bigger[i][0] * holes_bigger[i + 1][1] - holes_bigger[i + 1][0] * holes_bigger[i][1]

    size_bigger = int((abs(size_bigger) + perimeter) / 2) + 1
    print(size_bigger)
