import math


PUZZLE_INPUT = 34000000
HOUSES = 50


def find_divisors(n):
    divisors = set()
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divisors.add(i)
            divisors.add(n // i)

    return list(divisors)


def part_one():
    house_number = 1
    while True:
        presents = sum(map(lambda x: x * 10, find_divisors(house_number)))

        if presents >= PUZZLE_INPUT:
            break

        house_number += 1

    return house_number


def part_two():
    def find_divisors_short(n):
        divisors = set()
        for i in range(1, int(math.sqrt(n)) + 1):
            if n % i == 0:
                if i > n // HOUSES or (i == n // HOUSES and n % HOUSES == 0):
                    divisors.add(i)
                if (n // i) > n // HOUSES or ((n // i) == n // HOUSES and n % HOUSES == 0):
                    divisors.add(n // i)

        return list(divisors)

    house_number = 1
    while True:
        elves = find_divisors_short(house_number)
        presents = sum(map(lambda x: x * 11, elves))

        if presents >= PUZZLE_INPUT:
            break

        house_number += 1

    return house_number


print(part_one())
print(part_two())
