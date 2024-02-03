from itertools import permutations


with open('9.txt', 'r') as f:
    distances_input = [s.strip() for s in f.readlines()]

    locations_distances = dict()

    for d in distances_input:
        locations, distance = [i.strip() for i in d.split('=')]
        l1, l2 = [l.strip() for l in locations.split('to')]

        if l1 not in locations_distances.keys():
            locations_distances[l1] = dict()
        if l2 not in locations_distances.keys():
            locations_distances[l2] = dict()

        locations_distances[l1][l2] = int(distance)
        locations_distances[l2][l1] = int(distance)

    # Looks like cheating but why not!
    # I hope this works fine and fast. Yep, it does
    routes = list(permutations(locations_distances.keys(), len(locations_distances.keys())))


def part_one():
    min_distance = 1000000000  # Some big number
    for r in routes:
        r_distance = 0
        for i in range(1, len(r)):
            from_, to_ = r[i - 1], r[i]
            r_distance += locations_distances[to_][from_]
        min_distance = min(min_distance, r_distance)

    return min_distance


def part_two():
    max_distance = 0
    for r in routes:
        r_distance = 0
        for i in range(1, len(r)):
            from_, to_ = r[i - 1], r[i]
            r_distance += locations_distances[to_][from_]
        max_distance = max(max_distance, r_distance)

    return max_distance


print(part_one())
print(part_two())
