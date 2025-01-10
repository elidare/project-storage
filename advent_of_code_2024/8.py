antenna_map = list()
antennas = dict()

with open('8.txt', 'r') as f:
    for (i, line) in enumerate(f):
        line = line.strip()
        antenna_map.append(line)  # Appending the current row to the map

        # Search through the row and put all the antennas and their coordinates into a dict
        for j in range(len(line)):
            if line[j] == '.':
                continue
            if line[j] not in antennas:
                antennas[line[j]] = [(i, j)]
            else:
                antennas[line[j]].append((i, j))

size_m = len(antenna_map)
size_n = len(antenna_map[0])


def get_antinodes():
    antinodes = set()
    for positions in antennas.values():
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                # Calculate the diff between the positions
                x_diff, y_diff = positions[i][0] - positions[j][0], positions[i][1] - positions[j][1]
                # The antinodes are located either farther behind the farther antenna,
                # or closer in front of the closer one
                possible_antinodes = [(positions[i][0] + x_diff, positions[i][1] + y_diff),
                                      (positions[j][0] - x_diff, positions[j][1] - y_diff)]
                for pa in possible_antinodes:
                    if 0 <= pa[0] < size_m and 0 <= pa[1] < size_n:
                        antinodes.add(pa)
    return antinodes


def get_antinodes_with_harmonics():
    antinodes_harmonics = set()
    for positions in antennas.values():
        if len(positions) == 1:
            # If the antenna is the only one of its frequency, skip it
            continue

        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                # Calculate the diff between the positions
                x_diff, y_diff = positions[i][0] - positions[j][0], positions[i][1] - positions[j][1]
                # Let's count all the possible antinodes in two whiles - backward and forward
                possible_antinode = positions[i][0], positions[i][1]
                while 0 <= possible_antinode[0] < size_m and 0 <= possible_antinode[1] < size_n:
                    antinodes_harmonics.add(possible_antinode)
                    possible_antinode = possible_antinode[0] + x_diff, possible_antinode[1] + y_diff

                possible_antinode = positions[j][0], positions[j][1]
                while 0 <= possible_antinode[0] < size_m and 0 <= possible_antinode[1] < size_n:
                    antinodes_harmonics.add(possible_antinode)
                    possible_antinode = possible_antinode[0] - x_diff, possible_antinode[1] - y_diff

    return antinodes_harmonics


print('Unique antinode locations:', len(get_antinodes()))
print('Unique antinode with harmonics locations:', len(get_antinodes_with_harmonics()))
