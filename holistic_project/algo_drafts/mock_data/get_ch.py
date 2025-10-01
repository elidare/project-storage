import requests
import json


def get_lat_lon(address):
    # Using Nominatim API
    lat = lon = 0

    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': address,
        'format': 'json',
        'limit': 1  # get only the best match
    }

    headers = {'User-Agent': 'github/elidare'}

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    if data:
        lat = data[0]['lat']
        lon = data[0]['lon']

    return lat, lon


chargers = []

# Used a list of chargers copied from Chargefinder
# with open('ch_mock_2', 'a') as mock:
#     with open('ch_mock', 'r') as f:
#         for row in f:
#             row = row.strip()
#
#             if row.startswith('<'):
#                 continue
#
#             mock.write(row.replace('</a>', '').replace('</div>', ''))
#             mock.write('\n')
#
#             if not row:
#                 break

with open('ch_mock_2', 'r', encoding='utf-8') as f:
    lines = [l.strip() for l in f.readlines()]

    for i in range(0, len(lines), 5):
        name = lines[i]
        address = lines[i + 2]
        type = lines[i + 3]
        op_power = lines[i + 4]  # Todo
        lat, lon = [float(n) for n in get_lat_lon(address)]  # Todo check if works

        if lat == 0 or lon == 0:
            continue

        chargers.append({
            'name': name,
            'address': address,
            'type': type,
            'op_power': op_power,
            'lat': lat,
            'lon': lon,
            'coords': (lon, lat)
        })

        print(f'Got {i}: {address}, {lat}, {lon}')

with open('chargers.json', 'w', encoding='utf-8') as f:
    json.dump(chargers, f, ensure_ascii=False, indent=4)
