# Part 1 works
# Part 2 does not. I'll skip it and look at it later at reddit

with open('19.txt', 'r') as f:
    lines = f.readlines()
    replacements = [[l.strip() for l in a.strip().split('=>')] for a in lines[:-2]]
    formula = lines[-1]


def part_one():
    distinct_molecules = list()

    for r in replacements:
        original, replacement = r
        index = formula.find(original)
        while index > -1:
            new_molecule = formula[:index] + replacement + formula[index + len(original):]
            distinct_molecules.append(new_molecule)
            index = formula.find(original, index + 1)

    return len(set(distinct_molecules))


def part_two_2():
    queue = [[formula]]  # Let's keep all the steps in a list and make a queue out of them
    min_steps = 1_000_000_000  # Some big value

    while queue:
        print('Queue length: ', len(queue))
        # print('queue____', queue)
        formulas = queue.pop()
        molecule = formulas[-1]
        print(molecule, len(formulas))

        if molecule == 'e':
            steps = len(formulas) - 1
            print('Minimum steps: ', steps)
            min_steps = min(steps, min_steps)
            continue

        for r in replacements:
            original, replacement = r
            index = molecule.find(replacement)

            while index > -1:
                # print('Inside while', index)
                print('FIND: ', replacement, original)
                new_molecule = molecule[:index] + original + molecule[index + len(replacement):]
                if new_molecule != molecule and new_molecule not in formulas:
                    formulas_copy = formulas[:]
                    formulas_copy.append(new_molecule)
                    print('______________ new_molecule', new_molecule)
                    queue.append(formulas_copy)

                index = molecule.find(replacement, index + 1)

    return min_steps


def part_two():
    queue = [(formula, 0)]
    min_steps = 1_000_000_000  # Some big value
    formulas_steps = dict()
    formulas_steps[formula] = 0
    dead_end = list()

    while queue:
        print('Queue length: ', len(queue))
        current_molecule, current_steps = queue.pop()
        print(current_molecule, current_steps)
        if (current_molecule, current_steps) in dead_end:
            continue

        if current_molecule == 'e':
            print('Minimum steps: ', current_steps)
            min_steps = min(current_steps, min_steps)
            continue

        found = False
        for r in replacements:
            original, replacement = r
            index = current_molecule.find(replacement)

            while index > -1:
                found = True
                new_molecule = current_molecule[:index] + original + current_molecule[index + len(replacement):]

                # if formulas_steps.get(new_molecule) and formulas_steps.get(new_molecule) <= current_steps + 1 \
                #         or new_molecule == current_molecule:
                #     continue
                # if new_molecule != current_molecule:
                print('new_molecule', new_molecule)
                # formulas_steps[new_molecule] = current_steps + 1
                if (new_molecule, current_steps + 1) not in queue:
                    queue.append((new_molecule, current_steps + 1))
                index = current_molecule.find(replacement, index + 1)
        else:
            # fixme how to mark a dead-end molecule
            if not found:
                print('NOT FOUND_____', current_molecule, current_steps)
                dead_end.append((current_molecule, current_steps))

    return min_steps



# print(part_one())
print(part_two())
