from itertools import combinations, product


SHOP = {
    'Weapons': {
        'Dagger': {'Cost': 8, 'Damage': 4, 'Armor': 0},
        'Shortsword': {'Cost': 10, 'Damage': 5, 'Armor': 0},
        'Warhammer': {'Cost': 25, 'Damage': 6, 'Armor': 0},
        'Longsword': {'Cost': 40, 'Damage': 7, 'Armor': 0},
        'Greataxe': {'Cost': 74, 'Damage': 8, 'Armor': 0}
    },
    'Armor': {
        'Leather': {'Cost': 13, 'Damage': 0, 'Armor': 1},
        'Chainmail': {'Cost': 31, 'Damage': 0, 'Armor': 2},
        'Splintmail': {'Cost': 53, 'Damage': 0, 'Armor': 3},
        'Bandedmail': {'Cost': 75, 'Damage': 0, 'Armor': 4},
        'Platemail': {'Cost': 102, 'Damage': 0, 'Armor': 5}
    },
    'Rings': {
        'Damage +1': {'Cost': 25, 'Damage': 1, 'Armor': 0},
        'Damage +2': {'Cost': 50, 'Damage': 2, 'Armor': 0},
        'Damage +3': {'Cost': 100, 'Damage': 3, 'Armor': 0},
        'Defense +1': {'Cost': 20, 'Damage': 0, 'Armor': 1},
        'Defense +2': {'Cost': 40, 'Damage': 0, 'Armor': 2},
        'Defense +3': {'Cost': 80, 'Damage': 0, 'Armor': 3}
    }
}


def get_play_costs():
    weapons = list(SHOP['Weapons'].keys())
    armor = list(SHOP['Armor'].keys()) + ['']  # As armor is optional
    rings = list(combinations(SHOP['Rings'].keys(), 2)) + \
            list(map(lambda x: (x, ''), SHOP['Rings'].keys())) + [('', '')]

    variants = list(product(weapons, armor, rings))  # (weapon, armor, (ring_1, ring_2))
    min_cost = 1_000_000  # Some big number
    max_cost = 0

    for variant in variants:
        player = {'HP': 100, 'Damage': 0, 'Armor': 0}
        # Do not commit real boss input:
        boss = {'HP': 100, 'Damage': 0, 'Armor': 0}

        current_weapon = SHOP['Weapons'][variant[0]]
        current_armor = SHOP['Armor'][variant[1]] if variant[1] else {}
        current_ring_1 = SHOP['Rings'][variant[2][0]] if variant[2][0] else {}
        current_ring_2 = SHOP['Rings'][variant[2][1]] if variant[2][1] else {}

        current_cost = current_weapon['Cost']
        player['Damage'] = current_weapon['Damage']

        if current_armor:
            current_cost += current_armor['Cost']
            player['Armor'] += current_armor['Armor']

        if current_ring_1:
            current_cost += current_ring_1['Cost']
            player['Damage'] += current_ring_1['Damage']
            player['Armor'] += current_ring_1['Armor']

        if current_ring_2:
            current_cost += current_ring_2['Cost']
            player['Damage'] += current_ring_2['Damage']
            player['Armor'] += current_ring_2['Armor']

        while True:
            # Player hits
            boss['HP'] -= player['Damage'] - boss['Armor']

            if boss['HP'] <= 0:
                min_cost = min(min_cost, current_cost)  # Part 1
                break

            # Boss hits
            player['HP'] -= boss['Damage'] - player['Armor']

            if player['HP'] <= 0:
                max_cost = max(max_cost, current_cost)  # Part 2
                break

    return min_cost, max_cost


print(*get_play_costs())
