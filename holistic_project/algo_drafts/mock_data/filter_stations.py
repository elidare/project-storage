from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import json


# ⚙️ Define an 8-point polygon (lon, lat) — note the order!
polygon_coords = [
    (23.087028632520255, 60.19864212395437),  # Perniö
    (22.177048002999623, 60.43319356383104),  # Turku
    (23.596610656213162, 61.5506413110826),  # Ylöjärvi
    (25.735148955152525, 62.29429764188131),  # Jyväskylä
    (27.58897646733634, 61.7827395355478),  # Mikkeli
    (29.02669878805264, 61.292782079954804),  # Imatra
    (27.055424132062562, 60.37544733337039),  # Kotka
    (25.01830576652588, 60.0965974716036)  # Helsinki
]

polygon = Polygon(polygon_coords)

new_stations = []
cuisines_dict = {}
restaurant_names = set()  # restaurant.name
restaurant_doubles = set()  # restaurant.name, restaurant.address

# Plot polygon
# x, y = zip(*polygon_coords)
# plt.plot(x + (x[0],), y + (y[0],), 'b-', label='Polygon Area')

with open('stations_restaurants_fixed_cuisines.json', 'r', encoding='utf-8') as data:
    stations = json.load(data)
    i = 1
    for s in stations:
        if polygon.contains(Point(s['lon'], s['lat'])):
            del s['coords']

            filtered = []
            seen_cuisines = set()
            for r in s['restaurants']:
                del r['coords']
                # Rename Unnamed restaurant
                if r['name'] == 'Unnamed restaurant':
                    r['name'] = ' '.join(s['name'].split()[:1]) + f' {i} Restaurant'
                if r['address'] == 'Not provided':
                    r['address'] = s['address']

                # If there are >1 restaurants with the same name and the same address, add only one
                if (r['name'], r['address']) in restaurant_doubles:
                    continue
                restaurant_doubles.add((r['name'], r['address']))

                # If there are >1 restaurants with the same name but different address, add second with a number
                if r['name'] in restaurant_names:
                    r['name'] += f' {i}'
                restaurant_names.add(r['name'])

                for cuisine in r["cuisine"]:
                    # Save restaurant only with unique cuisine for this station
                    if cuisine not in seen_cuisines:
                        seen_cuisines.add(cuisine)
                        filtered.append(r)
                        break  # stop after adding the restaurant once

            s['restaurants'] = filtered
            if len(s['restaurants']) == 0:
                continue

            # Update station name
            s['name'] = f'Feast-faster {i} ' + ' '.join(s['name'].split()[2:])
            new_stations.append(s)
            i += 1

            # for r in s['restaurants']:
            #     for c in r['cuisine']:
            #         cn = cuisines_dict.get(c, 0)
            #         cuisines_dict[c] = cn + 1

        # plt.scatter(s['lon'], s['lat'], color='green' if polygon.contains(Point(s['lon'], s['lat'])) else 'red')

print(len(stations), sum(list([len(s['restaurants']) for s in stations])),
      len(new_stations), sum(list([len(s['restaurants']) for s in new_stations])))

with open('stations_restaurants_shortened.json', 'w', encoding='utf-8') as f:
    json.dump(new_stations, f, ensure_ascii=False, indent=4)


# print(cuisines_dict)
# {'turkish': 76, 'regional': 45, 'asian': 167, 'european': 61, 'american': 90, 'mexican': 57, 'italian': 148, 'vegetarian': 47}

# for s in new_stations:
#     for r in s['restaurants']:
#         for c in r['cuisine']:
#             cn = cuisines_dict.get(c, 0)
#             cuisines_dict[c] = cn + 1
# print(cuisines_dict)
# {'turkish': 67, 'regional': 33, 'asian': 58, 'european': 49, 'american': 57, 'mexican': 36, 'italian': 88, 'vegetarian': 34}

# plt.xlabel("Longitude")
# plt.ylabel("Latitude")
# plt.legend()
# plt.title("Places within polygon area")
#
# # ✅ Save plot as file
# plt.savefig("filtered_places.png", dpi=300, bbox_inches="tight")

# rest_names = set()
# for s in new_stations:
#     for r in s['restaurants']:
#         if r['name'] in rest_names:
#             print(r['name'], r['address'])
#         rest_names.add(r['name'])
