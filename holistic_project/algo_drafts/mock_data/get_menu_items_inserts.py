import random
import json

cuisines = ['american', 'european', 'mexican', 'vegetarian', 'regional', 'asian', 'turkish', 'italian']
categories = ["Mains", "Snacks", "Beverages"]
menu_items_values = []
number_of_meals = 0


with open('menu_items_mock.json', 'r', encoding='utf-8') as file:
    menu_items = json.load(file)


with open('stations_restaurants_shortened.json', 'r', encoding='utf-8') as stations:
    stations = json.load(stations)

    for st in stations:
        for r in st["restaurants"]:
            restaurant_name = r['name'].replace("'", "''")
            # If restaurant serves different cuisines, take 1 meal of each category, else 2 meals of each category
            number_of_meals = 2 if len(r["cuisine"]) == 1 else 1

            for c in r["cuisine"]:
                for cat in categories:
                    items = random.sample(menu_items[c][cat], number_of_meals)
                    for item in items:
                        menu_items_values.append(f"('{restaurant_name}', "
                                                 f"'{item["name"]}', "
                                                 f"'{item["details"]}', "
                                                 f"{item["price"]}, "
                                                 f"{item["minutes_to_prepare"]}, "
                                                 f"'available', "
                                                 f"'{cat}')")


with open('inserts_menu_items', 'a', encoding='utf-8') as file:
    menu_items_insert = f"""
INSERT INTO menu_items (restaurant_id, name, details, price, minutes_to_prepare, availability, category)
SELECT r.restaurant_id, v.name, v.details, v.price, v.minutes_to_prepare, v.availability::menu_item_availability, v.category::food_category
FROM (
  VALUES
    {',\n'.join(menu_items_values)}
) AS v(restaurant_name, name, details, price, minutes_to_prepare, availability, category)
JOIN restaurants r
ON r.name = v.restaurant_name;"""

    file.write(menu_items_insert)
