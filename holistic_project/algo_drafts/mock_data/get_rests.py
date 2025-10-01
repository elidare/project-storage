# Get restaurant list with OpenStreetMap
# https://www.openstreetmap.org/
# https://chatgpt.com/share/68dd52a9-c808-8003-b7c1-01709e73b369


import requests
import json

# Coordinates (example: Lahti, Finland)
lat, lon = 60.9827, 25.6612


# Overpass query: restaurants within N m
around = 5000  # m
query = f'''
[out:json];
(
  node['amenity'='restaurant'](around:{around},{lat},{lon});
  way['amenity'='restaurant'](around:{around},{lat},{lon});
  relation['amenity'='restaurant'](around:{around},{lat},{lon});
);
out center;
'''

url = 'http://overpass-api.de/api/interpreter'
response = requests.get(url, params={'data': query})
data = response.json()

restaurants = []

for element in data['elements']:
    tags = element.get('tags', {})
    name = tags.get('name', 'Unnamed restaurant')
    lat = element.get('lat') or element.get('center', {}).get('lat')
    lon = element.get('lon') or element.get('center', {}).get('lon')
    lat, lon = float(lat), float(lon)

    # Build address from tags
    street = tags.get('addr:street', '')
    housenumber = tags.get('addr:housenumber', '')
    city = tags.get('addr:city', '')

    address = ' '.join([street, housenumber]).strip()
    if city:
        address = f'{address}, {city}' if address else city

    cuisine = tags.get('cuisine', 'Unknown')

    if lat and lon:
        restaurants.append({
            'name': name,
            'lat': lat,
            'lon': lon,
            'address': address if address else 'Not provided',
            'cuisine': cuisine,
            'coords': (lon, lat)
        })

with open('restaurants.json', 'w', encoding='utf-8') as f:
    json.dump(restaurants, f, ensure_ascii=False, indent=4)

print('Saved')
