with open('2.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]
    max_cubes = {'red': 12, 'green': 13, 'blue': 14}
    result = 0
    result_2 = 0

    for line in lines:
        line_parts = line.split(':')
        game_number = int(line_parts[0].replace('Game ', ''))
        games = line_parts[1].strip().split(';')
        can_be_played = True
        # Part 1
        for rnd in games:
            cubes = rnd.split(',')
            for colour_type in cubes:
                num, colour = colour_type.strip().split()[0], colour_type.strip().split()[1]
                if int(num) > max_cubes[colour]:
                    can_be_played = False
                    break
        if can_be_played:
            result += int(game_number)

        # Part 2
        min_cubes = {'red': 0, 'green': 0, 'blue': 0}
        for rnd in games:
            cubes = rnd.split(',')
            for colour_type in cubes:
                num, colour = colour_type.strip().split()[0], colour_type.strip().split()[1]
                if int(num) > min_cubes[colour]:
                    min_cubes[colour] = int(num)
        power = 1
        for cubes_num in min_cubes.values():
            power *= cubes_num
        result_2 += power

    print(result)
    print(result_2)

