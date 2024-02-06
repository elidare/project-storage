with open('14.txt', 'r') as f:
    input = [s.strip() for s in f.readlines()]
    deer_dict = dict()
    RACE_TIME = 2503

    for i in input:
        parts = i.split(' ')
        name = parts[0]
        speed, flying, resting = list(map(int, filter(lambda x: x.isnumeric(), parts)))
        deer_dict[name] = {'speed': speed, 'flying': flying, 'resting': resting, 'points': 0, 'current_distance': 0}


def part_one():
    def get_distance(name, time):
        d = deer_dict[name]
        cycle_time = d['flying'] + d['resting']
        flying_full_cycles = time // cycle_time
        flying_seconds = flying_full_cycles * d['flying'] + min(time - flying_full_cycles * cycle_time, d['flying'])
        return flying_seconds * d['speed']

    max_distance = 0
    for d in deer_dict.keys():
        max_distance = max(max_distance, get_distance(d, RACE_TIME))

    return max_distance


def part_two():
    def move_deer(deer, second):
        second = second % (deer['flying'] + deer['resting'])
        if 0 < second <= deer['flying']:
            deer['current_distance'] += deer['speed']

    for i in range(1, RACE_TIME + 1):
        for deer in deer_dict.values():
            move_deer(deer, i)

        max_distance = max([d['current_distance'] for d in deer_dict.values()])

        for deer in deer_dict.values():
            # In case several deer have travelled the same distance
            if deer['current_distance'] == max_distance:
                deer['points'] += 1

    return max([d['points'] for d in deer_dict.values()])


print(part_one())
print(part_two())
