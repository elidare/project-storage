import re
import json


with open('12.txt', 'r') as f:
    json_ = f.readline()
    structure = json.loads(json_)


def part_one():
    return sum([int(n) for n in re.findall('-?\\d+', json_)])


# Advent 2023 taught me to use queues everywhere, so here we are, done in about 20 minutes
def part_two():
    RED = 'red'
    # Taken as granted that the given data is an array
    queue = structure
    total_count = 0

    while queue:
        current_object = queue.pop()
        if isinstance(current_object, list):
            queue += current_object
        elif isinstance(current_object, dict):
            if RED not in current_object.values():
                queue += current_object.values()
        elif isinstance(current_object, int):
            total_count += current_object

    return total_count


print(part_one())
print(part_two())
