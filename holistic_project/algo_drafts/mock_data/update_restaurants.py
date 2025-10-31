import json
import random

cuisine_mapping = {
'western': 'american',
'tex-mex': 'mexican',
'burger': 'american',
'drinks': 'american',
'fish_and_chips': 'european',
'sandwich': 'european',
'poke': 'asian',
'malaysian': 'asian',
'hamburger': 'american',
'wings': 'american',
'brunch': 'european',
'deli': 'asian',
'kasvislounas': 'vegetarian',
'japanese': 'asian',
'fried_chicken': 'american',
'viking': 'european',
'steak_house': 'american',
'greek': 'regional',
'ethiopian': 'regional',
'coffee_shop': 'european',
'indian': 'asian',
'lunch': 'european',
'buffet': 'european',
'bangladeshian': 'asian',
'salad': 'vegetarian',
'ice_cream': 'vegetarian',
'georgian': 'regional',
'afghan': 'regional',
'eritrean': 'regional',
'fast_food': 'american',
'regional': 'european',
'indonesian': 'asian',
'diner': 'american',
'pizza': 'italian',
'soup': 'european',
'chicken': 'american',
'nepalese': 'asian',
'chinese': 'asian',
'grill': 'american',
'sri lanka': 'asian',
'mediterranean': 'european',
'pasta': 'italian',
'international': 'regional',
'noodle': 'asian',
'bistro': 'european',
'barbecue': 'american',
'kebab': 'turkish',
'ribs': 'american',
'pancake': 'american',
'persian': 'regional',
'korean': 'asian',
'italian_pizza': 'italian',
'juice': 'vegetarian',
'vietnamese': 'asian',
'pastry': 'european',
'finnish': 'european',
'hawaiian': 'regional',
'french': 'european',
'tacos': 'mexican',
'sausage': 'american',
'breakfast': 'vegetarian',
'ramen': 'asian',
'local': 'european',
'thai': 'asian',
'fish': 'european',
'spanish': 'european',
'balkan': 'regional',
'coffee': 'regional',
'fine_dining': 'european',
'steak': 'american',
'waffle': 'american',
'sushi': 'asian',
'argentinian': 'mexican'
}

cuisines = ['american', 'european', 'mexican', 'vegetarian', 'regional', 'asian', 'turkish', 'italian']

new_stations = []

with open('stations_restaurants_initial.json', 'r', encoding='utf-8') as stations:
    data = json.load(stations)
    for st in data:
        if len(st['restaurants']):
            for r in st['restaurants']:
                r_cuisines = set()
                r['cuisine'] = r['cuisine'].split(';')
                for c in r['cuisine']:
                    if c == 'Unknown':
                        c = random.choice(cuisines)
                    elif c in cuisine_mapping:
                        c = cuisine_mapping[c]

                    r_cuisines.add(c)

                r['cuisine'] = list(r_cuisines)
            new_stations.append(st)

# Drop to another file and filter out stations only with restaurants
with open('stations_restaurants_fixed_cuisines.json', 'w', encoding='utf-8') as f:
    json.dump(new_stations, f, ensure_ascii=False, indent=4)
