with open('3.txt', 'r') as f:
    input = list(f.readline())
    directions = {'^': [-1, 0], 'v': [1, 0], '<': [0, -1], '>': [0, 1]}

    def part_one():
        visited = list()
        visited.append((0, 0))  # Starting point

        for i in input:
            last_point = visited[-1]
            new_x, new_y = last_point[0] + directions[i][0], last_point[1] + directions[i][1]
            visited.append((new_x, new_y))

        return len(set(visited))

    def part_two():
        visited_santa = list()
        visited_robo_santa = list()
        visited_santa.append((0, 0))  # Starting point
        visited_robo_santa.append((0, 0))  # Starting point

        for i, d in enumerate(input):
            santas_turn = i % 2 == 0
            visited = visited_santa[:] if santas_turn else visited_robo_santa[:]
            last_point = visited[-1]
            new_x, new_y = last_point[0] + directions[d][0], last_point[1] + directions[d][1]
            visited.append((new_x, new_y))
            if santas_turn:
                visited_santa = visited[:]
            else:
                visited_robo_santa = visited[:]

        return len(set(visited_santa + visited_robo_santa))

    # print(part_one())
    print(part_two())
