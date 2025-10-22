import requests
import json
import re
from bs4 import BeautifulSoup


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


def parse_html():
    # Chargefinder list of chargers, deleted first 2 divs, each station on a different row (row starts with <img ...)
    with open('ch_mock_2', 'a') as mock:
        with open('ch_mock', 'r') as f:
            for row in f:
                html = row.strip()
                # print(html)
                soup = BeautifulSoup(html, "html.parser")
                a_tags = soup.find_all("a", class_="link prevent-router")
                owner_divs = soup.find_all("div", class_="owner")

                texts = [tag.get_text(strip=True) for tag in a_tags + owner_divs]

                for text in texts:
                    mock.write(text)
                    mock.write('\n')


def get_origin_chargers():
    chargers_orig = {}

    with open('ch_mock_2', 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f.readlines()]

        for i in range(0, len(lines), 4):
            origin_name = lines[i]
            address = lines[i + 1]
            type = lines[i + 2]
            max_op_power = lines[i + 3]
            pattern = r'\b\d+(?:\.\d+)?\s*kW\b'  # matches numbers like 11 or 200 or 22.5 followed by kW
            match = re.search(pattern, max_op_power)
            max_op_power = match.group()

            lat, lon = [float(n) for n in get_lat_lon(address)]

            if lat == 0 or lon == 0:
                continue

            if origin_name not in chargers_orig:
                chargers_orig[origin_name] = {
                    'origin_name': origin_name,
                    'address': address,
                    'type': type,
                    'max_op_power': max_op_power,
                    'lat': lat,
                    'lon': lon,
                    'coords': (lon, lat)
                }

            print(f'Got {i / 4}: {address}, {lat}, {lon} out of {len(lines) / 4}')

    with open('chargers_original.json', 'w', encoding='utf-8') as f:
        json.dump(chargers_orig, f, ensure_ascii=False, indent=4)


def get_chargers():
    # We have original dict of chargers, now change the names to Feast faster to hide the real names
    with (open('chargers.json', 'w', encoding='utf-8') as f):
        chargers = []
        with open('chargers_original.json', 'r', encoding='utf-8') as orig:
            data = json.load(orig)
            i = 1
            for k, v in data.items():
                origin_name = v['origin_name']
                name = re.sub(r'ABC-lataus\sS-[Mm]arket|ABC-lataus|S-[Mm]arket|K-Market|K-Citymarket|K-Supermarket|K-Rauta', '', origin_name)
                name = f'Feast-faster {i} ' + name.strip()
                i += 1
                chargers.append({
                    'name': name,
                    'address': v['address'],
                    'type': v['type'],
                    'max_op_power': v['max_op_power'],
                    'lat': v['lat'],
                    'lon': v['lon'],
                    'coords': (v['lon'], v['lat'])
                })

            json.dump(chargers, f, ensure_ascii=False, indent=4)


# get_origin_chargers()
get_chargers()
