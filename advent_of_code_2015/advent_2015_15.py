# There should be some beautiful maths, but I have no idea which one
# I'll try bruteforce and have a glance at the reddit later

with open('15.txt', 'r') as f:
    input = [s.strip() for s in f.readlines()]
    ingredients = list()

    for l in input:
        name, quantity = [p.strip() for p in l.split(':')]
        ingredients.append({n.strip().split(' ')[0]: int(n.strip().split(' ')[1]) for n in quantity.split(',')})


def part_one():
    total_score = 0

    # There are 4 ingredients in the real input, so let's do some hardcode
    for i in range(1, 100):  # 1 <= spoons < 100
        for j in range(1, 100):
            for k in range(1, 100):
                l = 100 - i - j - k
                if l <= 0:
                    continue
                quantity = (i, j, k, l)
                capacity = durability = flavor = texture = 0

                for m in range(len(ingredients)):
                    capacity += ingredients[m]['capacity'] * quantity[m]
                    durability += ingredients[m]['durability'] * quantity[m]
                    flavor += ingredients[m]['flavor'] * quantity[m]
                    texture += ingredients[m]['texture'] * quantity[m]

                capacity = capacity if capacity >= 0 else 0
                durability = durability if durability >= 0 else 0
                flavor = flavor if flavor >= 0 else 0
                texture = texture if texture >= 0 else 0

                total_score = max(total_score, capacity * durability * flavor * texture)

    return total_score


def part_two():
    total_score = 0
    CALORIES = 500

    for i in range(1, 101):
        for j in range(1, 101):
            for k in range(1, 101):
                l = 100 - i - j - k
                if l <= 0:
                    continue
                quantity = (i, j, k, l)
                capacity = durability = flavor = texture = calories = 0

                for m in range(len(ingredients)):
                    capacity += ingredients[m]['capacity'] * quantity[m]
                    durability += ingredients[m]['durability'] * quantity[m]
                    flavor += ingredients[m]['flavor'] * quantity[m]
                    texture += ingredients[m]['texture'] * quantity[m]
                    calories += ingredients[m]['calories'] * quantity[m]

                if calories != CALORIES:
                    continue

                capacity = capacity if capacity >= 0 else 0
                durability = durability if durability >= 0 else 0
                flavor = flavor if flavor >= 0 else 0
                texture = texture if texture >= 0 else 0

                total_score = max(total_score, capacity * durability * flavor * texture)
    return total_score


print(part_one())
print(part_two())
