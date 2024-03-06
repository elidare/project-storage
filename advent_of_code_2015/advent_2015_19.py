# Part 1 works
# Part 2 does not work.
# I still haven't made it, I've tried reading reddit explanations, but with no success really
# Taken several solutions to get a star
# because I don't like unfinished business

# !! https://www.reddit.com/r/adventofcode/comments/3xflz8/comment/cy4etju/

from collections import deque


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


def part_two():
    # NOT WORKING CORRECTLY
    queue = deque([(formula, 0)])
    min_steps = 1_000_000_000  # Some big value

    replacements_sorted = sorted(replacements, key=lambda x: len(x[1]), reverse=True)

    while queue:
        current_molecule, current_steps = queue.pop()

        if current_molecule == 'e':
            print('Minimum steps: ', current_steps)
            min_steps = min(current_steps, min_steps)
            continue

        for r in replacements_sorted:
            original, replacement = r
            index = current_molecule.find(replacement)

            while index > -1:
                new_molecule = current_molecule[:index] + original + current_molecule[index + len(replacement):]
                if (new_molecule, current_steps + 1) not in queue:
                    queue.append((new_molecule, current_steps + 1))
                index = current_molecule.find(replacement, index + 1)

    return min_steps


def extra(basis):
    # https://www.reddit.com/r/adventofcode/comments/19eb08o/comment/kjdqeaw/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    # How the actual f__k?!
    rn = basis.count('Rn')
    ar = basis.count('Ar')
    yy = basis.count('Y')
    ele = sum(c < 'a' for c in basis)
    print("Part 2:", ele - rn - ar - yy - yy - 1)


print(part_one())
print(part_two())
