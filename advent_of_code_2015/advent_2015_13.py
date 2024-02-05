from itertools import permutations


with open('13.txt', 'r') as f:
    input = [s.strip() for s in f.readlines()]
    attendees = dict()

    for i in input:
        values = i[:-1].split(' ')  # Taken as granted the pattern of the input
        person, neighbour, happiness, indicator = values[0], values[10], values[3], values[2]

        if person not in attendees:
            attendees[person] = dict()

        attendees[person][neighbour] = int(happiness if indicator == 'gain' else '-' + happiness)


def get_seating(attendees):
    max_happiness = 0
    # Copy-paste Day 9
    arrangements = list(permutations(attendees.keys(), len(attendees.keys())))

    for arrangement in arrangements:
        total_happiness = 0
        for i in range(len(arrangement)):
            person, neighbour1, neighbour2 = arrangement[i], arrangement[i - 1], arrangement[i + 1 - len(arrangement)]
            total_happiness += attendees[person][neighbour1] + attendees[person][neighbour2]

        max_happiness = max(max_happiness, total_happiness)

    return max_happiness


# Part one
print(get_seating(attendees))

# Part two
for neighbours in attendees.values():
    neighbours['myself'] = 0

attendees['myself'] = {p: 0 for p in attendees.keys()}

print(get_seating(attendees))
