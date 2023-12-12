with open('11.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

    GALAXY = '#'
    EXPANSION = 1000000
    space = []
    galaxies = []
    rows_with_no_galaxies = []
    columns_with_no_galaxies = []

    # Part 1
    for i in range(len(lines)):
        line = lines[i]
        if not len(columns_with_no_galaxies):
            columns_with_no_galaxies = list(range(len(line)))
        space.append(line)
        if lines[i].find(GALAXY) == -1:
            rows_with_no_galaxies.append(i)
            continue
        for j in range(len(line)):
            if line[j] == GALAXY:
                galaxies.append((i, j))
                if j in columns_with_no_galaxies:
                    columns_with_no_galaxies.remove(j)

    # Count the paths
    result = 0
    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            # If there are any empty rows between 2 galaxies, add them up
            vertical_diff = abs(galaxies[j][0] - galaxies[i][0])
            horizontal_diff = abs(galaxies[j][1] - galaxies[i][1])
            if vertical_diff > 1:
                start = min(galaxies[i][0] + 1, galaxies[j][0])
                end = max(galaxies[i][0] + 1, galaxies[j][0])
                rows_between = set(range(start, end))
                rows_between_empty = rows_between.intersection(rows_with_no_galaxies)
                # vertical_diff += len(rows_between_empty)  # Part 1
                vertical_diff += (EXPANSION - 1) * len(rows_between_empty)  # Part 2
            if horizontal_diff > 1:
                start = min(galaxies[i][1] + 1, galaxies[j][1])
                end = max(galaxies[i][1] + 1, galaxies[j][1])
                columns_between = set(range(start, end))
                columns_between_empty = columns_between.intersection(columns_with_no_galaxies)
                # horizontal_diff += len(columns_between_empty)  # Part 1
                horizontal_diff += (EXPANSION - 1) * len(columns_between_empty)  # Part 2

            shortest_path = vertical_diff + horizontal_diff
            result += shortest_path
    print('result', result)
