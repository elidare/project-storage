with open('9.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]
    result_1 = 0
    result_2 = 0

    def predict_next_diff(sequence):
        next_array = []
        for i in range(len(sequence) - 1):
            next_array.append(sequence[i + 1] - sequence[i])
        if all([n == 0 for n in next_array]):
            return 0
        next_number = predict_next_diff(next_array)
        next_array.append(next_array[-1] + next_number)
        return next_array[-1]

    def predict_previous_diff(sequence):
        next_array = []
        for i in range(len(sequence) - 1):
            next_array.append(sequence[i + 1] - sequence[i])
        if all([n == 0 for n in next_array]):
            return 0
        next_number = predict_previous_diff(next_array)
        next_array.insert(0, next_array[0] - next_number)
        return next_array[0]


    for line in lines:
        value_row = [int(n) for n in line.split()]
        # Part 1
        next_number = value_row[-1] + predict_next_diff(value_row)
        result_1 += next_number

        # Part 2
        previous_number = value_row[0] - predict_previous_diff(value_row)
        result_2 += previous_number

    print(result_1)
    print(result_2)
