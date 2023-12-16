with open('15.txt', 'r') as f:
    strings = [s for s in f.readline().split(',')]
    boxes = dict()
    DASH = '-'
    EQUALS = '='

    def hash_algorithm(string):
        current_value = 0
        for s in string:
            current_value += ord(s)
            current_value *= 17
            current_value = current_value % 256

        return current_value

    # Part 1
    result = 0
    for s in strings:
        result += hash_algorithm(s)
    print(result)

    # Part 2
    for s in strings:
        if DASH in s:
            label = s.replace(DASH, '')
            box_num = hash_algorithm(label)
            if box_num in boxes.keys() and label in boxes[box_num]:
                del boxes[box_num][label]
        else:
            label, focal_length = s.split(EQUALS)[0], int(s.split(EQUALS)[1])
            box_num = hash_algorithm(label)
            if box_num in boxes.keys():
                boxes[box_num][label] = focal_length
            else:
                boxes[box_num] = {label: focal_length}

    focusing_power = 0
    for box_num, lenses in boxes.items():
        for i in range(len(lenses.keys())):
            focusing_power += (box_num + 1) * (i + 1) * lenses[list(lenses.keys())[i]]
    print(focusing_power)
