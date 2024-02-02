import sys


sys.setrecursionlimit(10000)

with open('7.txt', 'r') as f:
    combinations = f.readlines()


RSHIFT = 'RSHIFT'
LSHIFT = 'LSHIFT'
AND = 'AND'
OR = 'OR'
NOT = 'NOT'


def part_one_two():
    def operate(right):
        operation_strings = wires[right]['operation_line'].split(' ')

        if len(operation_strings) == 1:
            # 123 -> x or u -> zz
            if operation_strings[0].isnumeric():
                x = int(operation_strings[0])
            else:
                x = wires[operation_strings[0]].get('value') or operate(operation_strings[0])
            wires[right]['value'] = x
        elif len(operation_strings) == 2:
            # NOT
            x = wires[operation_strings[1]].get('value') or operate(operation_strings[1])
            wires[right]['value'] = ~ x & 65535
        else:
            # All the other operations
            operation = operation_strings[1]
            if operation_strings[0].isnumeric():
                x = int(operation_strings[0])
            else:
                x = wires[operation_strings[0]].get('value') or operate(operation_strings[0])
            if operation_strings[2].isnumeric():
                y = int(operation_strings[2])
            else:
                y = wires[operation_strings[2]].get('value') or operate(operation_strings[2])

            if operation == RSHIFT:
                wires[right]['value'] = x >> y
            elif operation == LSHIFT:
                wires[right]['value'] = x << y
            elif operation == AND:
                wires[right]['value'] = x & y
            else:  # OR
                wires[right]['value'] = x | y

        return wires[right]['value']

    wires = {}  # 'value': 0, 'operation_line: None

    for c in combinations:
        left, right = [s.strip() for s in c.split('->')]
        wires[right] = {'operation_line': left}

    return operate('a')


print(part_one_two())
