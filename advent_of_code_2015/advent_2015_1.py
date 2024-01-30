with open('1.txt', 'r') as f:
    input = f.readline()
    DOWN = ')'
    UP = '('

    def part_one():
        count_down = input.count(DOWN)
        count_up = input.count(UP)
        return count_up - count_down

    def part_two():
        floor = 0
        for i in range(len(input)):
            floor = floor + 1 if input[i] == UP else floor - 1
            if floor < 0:
                return i + 1

    print(part_one())
    print(part_two())
