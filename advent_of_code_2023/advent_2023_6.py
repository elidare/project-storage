with open('6.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]
    result = 1

    # Part 1
    races = []
    for line in lines:
        if line.startswith('Time:'):
            times = line.split()[1:]
        elif line.startswith('Distance:'):
            distances = line.split()[1:]

    for i in range(0, len(times)):
        races.append({'time': int(times[i]), 'distance_record': int(distances[i])})

    for race in races:
        winning_ways = 0
        current_speed = 0
        total_time = race['time']
        for i in range(total_time + 1):
            longest_distance = (total_time - i) * i
            if longest_distance > race['distance_record']:
                winning_ways += 1

        result *= winning_ways
    print(result)

    # Part 2
    for line in lines:
        if line.startswith('Time:'):
            total_time_2 = int(line.replace('Time:', '').replace(' ', ''))
        elif line.startswith('Distance:'):
            record_distance = int(line.replace('Distance:', '').replace(' ', ''))

    winning_ways_2 = 0
    current_speed_2 = 0
    for i in range(total_time_2 + 1):
        longest_distance = (total_time_2 - i) * i
        if longest_distance > record_distance:
            winning_ways_2 += 1

    print(winning_ways_2)
