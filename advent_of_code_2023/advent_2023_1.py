with open('1.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]
    result = 0
    digit_str = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
                 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}

    # Part 1
    # for line in lines:
    #     digits = [s for s in line if s.isdigit()]
    #     digits = int(digits[0] + digits[-1])
    #     result += digits
    # print(result)

    # Part 2
    for line in lines:
        first_str_digit = len(line)
        last_str_digit = -1
        first_digit_to_replace = last_digit_to_replace = ''
        for d in digit_str.keys():
            index_first = line.find(d)
            if -1 < index_first < first_str_digit:
                first_str_digit = index_first
                first_digit_to_replace = d
            index_last = line.rfind(d)
            if index_last > last_str_digit:
                last_str_digit = index_last
                last_digit_to_replace = d
        digits = ''
        for i in range(0, len(line)):
            if line[i].isdigit():
                digits += line[i] if i < first_str_digit else digit_str[first_digit_to_replace]
                break
        for i in range(len(line) - 1, -1, -1):
            if line[i].isdigit():
                digits += line[i] if i > last_str_digit else digit_str[last_digit_to_replace]
                break
        result += int(digits)

    print(result)
