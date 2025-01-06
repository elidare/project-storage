# Part 2 takes about 2 minutes to calculate x.x

from itertools import product


def combined_result_part_1(line):
    test_value, nums = int(line.split(':')[0]), [int(n) for n in line.split(':')[1].split()]

    # e. g., (+, +), (+, *), (*, +), (*, *) for 3 numbers
    possible_combinations = list(product(['+', '*'], repeat=len(nums)-1))

    for pc in possible_combinations:
        result = nums[0]
        for i in range(len(nums) - 1):
            result = eval(str(result) + pc[i] + str(nums[i + 1]))

        if result == test_value:  # If at least one of the equations is true, return test value
            return test_value

    return 0  # If the line is not combined with operators, just return 0


def combined_result_part_2(line):
    test_value, nums = int(line.split(':')[0]), [int(n) for n in line.split(':')[1].split()]

    possible_combinations = list(product(['+', '*', '||'], repeat=len(nums)-1))

    for pc in possible_combinations:
        result = nums[0]
        for i in range(len(nums) - 1):
            if pc[i] == '||':
                result = int(str(result) + str(nums[i + 1]))
            else:
                result = eval(str(result) + pc[i] + str(nums[i + 1]))

        if result == test_value:  # If at least one of the equations is true, return test value
            return test_value

    return 0  # If the line is not combined with operators, just return 0


with open('7.txt', 'r') as f:
    calibrated_result_1 = 0
    calibrated_result_2 = 0
    while True:
        line = f.readline().strip()

        if not line:
            break

        calibrated_result_1 += combined_result_part_1(line)
        calibrated_result_2 += combined_result_part_2(line)

print('Result:', calibrated_result_1)
print('Result:', calibrated_result_2)
