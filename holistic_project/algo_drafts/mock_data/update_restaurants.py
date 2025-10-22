import json

with open('stations_restaurants_initial.json', 'r', encoding='utf-8') as stations:
    data = json.load(stations)
    cuisines = set()
    for st in data:
        if len(st['restaurants']):
            for r in st['restaurants']:
                r['cuisine'] = r['cuisine'].split(';')
                for c in r['cuisine']:
                    cuisines.add(c)
                    # todo update cuisines to a shorter list and update Unknown cuisine

print(cuisines)
# {'western', 'tex-mex', 'burger', 'drinks', 'fish_and_chips', 'sandwich', 'poke', 'malaysian', 'hamburger', 'wings', 'brunch', 'deli', 'kasvislounas', 'japanese', 'fried_chicken', 'viking', 'steak_house', 'Unknown', 'greek', 'ethiopian', 'coffee_shop', 'indian', 'mexican', 'lunch', 'buffet', 'bangladeshian', 'salad', 'ice_cream', 'georgian', 'afghan', 'eritrean', 'fast_food', 'regional', 'indonesian', 'diner', 'pizza', 'soup', 'chicken', 'nepalese', 'chinese', 'grill', 'sri lanka', 'mediterranean', 'asian', 'pasta', 'international', 'noodle', 'bistro', 'turkish', 'barbecue', 'kebab', 'ribs', 'pancake', 'persian', 'european', 'korean', 'italian', 'italian_pizza', 'juice', 'vietnamese', 'pastry', 'finnish', 'hawaiian', 'french', 'tacos', 'sausage', 'breakfast', 'ramen', 'local', 'thai', 'american', 'fish', 'spanish', 'balkan', 'coffee', 'fine_dining', 'steak', 'waffle', 'sushi', 'argentinian'}
