import math


with open('8.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

    directions = ''
    places = dict()
    starting_places = []

    for line in lines:
        if not directions:
            directions = line
            continue
        if line:
            places_draft = line.split('=')
            start, end = places_draft[0].strip(), places_draft[1].strip()
            end = end[1:-1].split(',')
            places[start] = {'L': end[0].strip(), 'R': end[1].strip()}
            if start.endswith('A'):
                starting_places.append(start)

    # Part 1
    next_place = 'AAA'
    finish = 'ZZZ'
    i = 0
    while True:
        current_direction = directions[i % len(directions)]
        next_place = places[next_place][current_direction]
        i += 1
        if next_place == finish:
            break
    print(i)

    # Part 2
    # Trying to solve it with LCM as said on reddit
    steps = []
    for place in starting_places:
        j = 0
        next_place = place
        while True:
            current_direction = directions[j % len(directions)]
            next_place = places[next_place][current_direction]
            j += 1
            if next_place.endswith('Z'):
                break
        steps.append(j)

    print(math.lcm(*steps))
