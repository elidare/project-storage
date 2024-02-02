with open('8.txt', 'r') as f:
    strings = [s.strip() for s in f.readlines()]


def part_one():
    total_count = 0
    memory_count = 0
    for s in strings:
        total_count += len(s)
        memory_count += len(eval(s))

    return total_count - memory_count


def part_two():
    total_count = 0
    escaped_count = 0
    for s in strings:
        total_count += len(s)
        escaped_count += len('"' + s.replace('\\', '\\\\').replace('\"', '\\"') + '"')

    return escaped_count - total_count


print(part_one())
print(part_two())
