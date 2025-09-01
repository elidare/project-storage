# Ofc I started with an array and ended up in some terribly long computations
# Searched thru reddit and made it a dictionary with count.
# Works much better now.
# https://www.reddit.com/r/adventofcode/comments/1hbm0al/2024_day_11_solutions/

with open('11.txt', 'r') as f:
    stones_given = f.readline().strip().split()
    stones = {}

    # Making dict of stones as {'stone_number': count}
    for s in stones_given:
        stones[s] = stones.get(s, 0) + 1


BLINKS = 25
BLINKS_2 = 75


def count_stones_dict(blinks, stones):
    for _ in range(blinks):
        stones_temp = {}

        for stone, count in stones.items():
            # Apply rules for stones
            if stone == '0':
                stones_temp['1'] = stones_temp.get('1', 0) + count
            elif len(stone) % 2 == 0:
                l = int(len(stone) / 2)
                stones_temp[str(int(stone[0:l]))] = stones_temp.get(str(int(stone[0:l])), 0) + count
                stones_temp[str(int(stone[l:]))] = stones_temp.get(str(int(stone[l:])), 0) + count
            else:
                stones_temp[str(int(stone) * 2024)] = stones_temp.get(str(int(stone) * 2024), 0) + count

        stones = stones_temp

    return sum(stones.values())


print(count_stones_dict(BLINKS, stones))  # Part 1
print(count_stones_dict(BLINKS_2, stones))  # Part 2
