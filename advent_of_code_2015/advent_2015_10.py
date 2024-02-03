with open('10.txt', 'r') as f:
    number = f.readline()


def convert(number):
    if len(number) == 1:
        return '1' + number

    new_number = ''
    count = 1
    current_number = ''
    for i in range(len(number)):
        if not current_number:
            current_number = number[i]
            continue
        if current_number == number[i]:
            count += 1
        else:
            new_number += str(count) + current_number
            current_number = number[i]
            count = 1

    new_number += str(count) + current_number

    return new_number


def convert_multiple(number, n):
    for i in range(n):
        number = convert(number)

    return len(number)


print(convert_multiple(number, 40))
print(convert_multiple(number, 50))
