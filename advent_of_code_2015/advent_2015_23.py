with open('23.txt', 'r') as f:
    instructions = [i.strip() for i in f.readlines()]


def count(registers):
    counter = 0
    while 0 <= counter < len(instructions):
        instruction = instructions[counter].split(' ')
        instr = instruction[0]
        if instr == 'jmp':
            counter = counter + int(instruction[1])
            continue

        reg = instruction[1][0:1]
        reg_value = registers[reg]
        if (instr == 'jie' and reg_value % 2 == 0) or (instr == 'jio' and reg_value == 1):
            counter = counter + int(instruction[2])
            continue
            
        if instr == 'hlf':
            reg_value = int(reg_value / 2)
        elif instr == 'inc':
            reg_value += 1
        elif instr == 'tpl':
            reg_value *= 3

        registers[reg] = reg_value
        counter += 1

    return registers


print(count({'a': 0, 'b': 0}))  # Part one
print(count({'a': 1, 'b': 0}))  # Part two
