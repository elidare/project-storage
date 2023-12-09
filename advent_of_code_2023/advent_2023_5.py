with open('5.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]
    seeds = []
    converter = {}  # {'seed': {'dst': 'soil', 'ranges': []}}
    converter_reversed = {}  # {'location': {'dst': 'humidity', 'ranges': []}}
    current_src = ''
    min_location = 0
    min_location_2 = 0

    def convert_number(src_number, ranges):
        for rng in ranges:
            if rng['src_range_start'] <= src_number < rng['src_range_start'] + rng['range_length']:
                return rng['dst_range_start'] + (src_number - rng['src_range_start'])
        return src_number

    for line in lines:
        if line.startswith('seeds'):
            seeds = [int(number) for number in line.split(':')[1].strip().split()]

        elif line.find('map:') > -1:
            items = line.split()[0].split('-')
            current_src = items[0]
            current_dst = items[2]
            converter[current_src] = {'dst': current_dst, 'ranges': []}
            converter_reversed[current_dst] = {'src': current_src, 'ranges': []}

        elif line:
            values = line.split()
            converter[current_src]['ranges'].append({
                'dst_range_start': int(values[0]),
                'src_range_start': int(values[1]),
                'range_length': int(values[2])
            })
            converter_reversed[current_dst]['ranges'].append({
                'dst_range_start': int(values[1]),
                'src_range_start': int(values[0]),  # To make it a bit more clear
                'range_length': int(values[2])
            })

    # Part 1:
    for seed_number in seeds:
        current_src = 'seed'
        src_number = seed_number

        while True:
            src_number = convert_number(src_number, converter[current_src]['ranges'])
            current_src = converter[current_src]['dst']
            if current_src == 'location':
                break

        if min_location > src_number or min_location == 0:
            min_location = src_number

    print('Minimum location:', min_location)

    # Part 2
    current_location = 0
    while not min_location_2:
        current_dst = 'location'
        current_number = current_location

        while True:
            current_number = convert_number(current_number, converter_reversed[current_dst]['ranges'])
            current_dst = converter_reversed[current_dst]['src']
            if current_dst == 'seed':
                break

        for i in range(0, len(seeds), 2):
            if seeds[i] <= current_number < seeds[i] + seeds[i + 1]:
                min_location_2 = current_location

        current_location += 1

    print('Minimum location:', min_location_2)
