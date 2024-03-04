from itertools import combinations


def multiply_list(given_list):
    # Multiply elements one by one
    result = 1
    for x in given_list:
        result = result * x
    return result


with open('24.txt', 'r') as f:
    packages = [int(p) for p in f.readlines()]


def part_one():
    variants = list()
    min_package_number = len(packages)
    min_quantum_entanglement = multiply_list(packages)

    # Making combinations of different divisions to 3 groups
    # I guess this is not really fast, but I am not able to calculate any algorithm
    for i in range(1, len(packages)):
        groups_1 = list(combinations(packages, i))

        # I don't need to calculate variants for the group, if its length is already bigger than minimum
        if i > min_package_number:
            break

        for g_1 in groups_1:
            # I would like to be sure that for this group 1 we really have at least one layout variant
            has_possible_variants = False

            # Group 1 weight should be 1/3 of the total weight
            if sum(list(g_1)) * 3 != sum(list(packages)):
                continue

            # If a possible group 1 is already bigger than a group with min packages, continue
            # We will still add several extra groups, but we'll sort them out later
            if len(list(g_1)) > min_package_number:
                continue

            group_2_3 = set(packages) - set(g_1)
            for j in range(1, len(group_2_3)):
                if has_possible_variants:
                    # We are not interested anymore
                    break

                groups_2 = list(combinations(group_2_3, j))
                for g_2 in groups_2:
                    # Group 2 weight should be 1/3 of the total weight
                    if sum(list(g_2)) * 3 != sum(list(packages)):
                        continue

                    # Now all the groups weigh 1/3 each, or equal as they have to be
                    group_1, group_2, group_3 = list(g_1), list(g_2), list(group_2_3 - set(g_2))
                    variants.append([group_1, group_2, group_3])

                    if len(group_1) < min_package_number:
                        min_package_number = len(group_1)

                    has_possible_variants = True
                    # We are not interested anymore
                    break

    # Calculating the best variant
    for v in variants:
        g_1, g_2, g_3 = v
        if len(g_1) > min_package_number:
            continue

        if multiply_list(g_1) < min_quantum_entanglement:
            min_quantum_entanglement = multiply_list(g_1)

    return min_quantum_entanglement


def part_two():
    variants = list()
    min_package_number = len(packages)
    min_quantum_entanglement = multiply_list(packages)

    # Making combinations of different divisions to 4 groups
    for i in range(1, len(packages)):
        groups_1 = list(combinations(packages, i))

        # I don't need to calculate variants for the group, if its length is already bigger than minimum
        if i > min_package_number:
            break

        for g_1 in groups_1:
            # I would like to be sure that for this group 1 we really have at least one layout variant
            has_possible_variants = False
            # Group 1 weight should be 1/4 of the total weight
            if sum(list(g_1)) * 4 != sum(list(packages)):
                continue

            # If a possible group 1 is already bigger than a group with min packages, continue
            # We will still add several extra groups, but we'll sort them out later
            if len(list(g_1)) > min_package_number:
                continue

            group_2_3_4 = set(packages) - set(g_1)
            for j in range(1, len(group_2_3_4)):
                if has_possible_variants:
                    # We are not interested anymore
                    break

                groups_2 = list(combinations(group_2_3_4, j))
                for g_2 in groups_2:
                    # Group 2 weight should be 1/4 of the total weight
                    if sum(list(g_2)) * 4 != sum(list(packages)):
                        continue

                    group_3_4 = set(group_2_3_4) - set(g_2)
                    for k in range(1, len(group_3_4)):
                        if has_possible_variants:
                            # We are not interested anymore
                            break

                        groups_3 = list(combinations(group_3_4, k))
                        for g_3 in groups_3:
                            # Group 3 weight should be 1/4 of the total weight
                            if sum(list(g_3)) * 4 != sum(list(packages)):
                                continue
                            # Now all the groups weigh 1/4 each, or equal as they have to be
                            group_1, group_2, group_3, group_4 = list(g_1), list(g_2), list(g_3), \
                                list(group_3_4 - set(g_3))
                            variants.append([group_1, group_2, group_3, group_4])

                            if len(group_1) < min_package_number:
                                min_package_number = len(group_1)

                            has_possible_variants = True
                            # We are not interested anymore
                            break

    # Calculating the best variant
    for v in variants:
        g_1, g_2, g_3, g_4 = v
        if len(g_1) > min_package_number:
            continue

        if multiply_list(g_1) < min_quantum_entanglement:
            min_quantum_entanglement = multiply_list(g_1)

    return min_quantum_entanglement


print(part_one())
print(part_two())
