import json


station_values = []
restaurant_values = []

with open('stations_restaurants_shortened.json', 'r', encoding='utf-8') as stations:
    stations = json.load(stations)
    for st in stations:
        station_values.append(f"('{st['name']}', "
                              f"ST_GeogFromText('SRID=4326;POINT({st['lon']} {st['lat']})'), "
                              f"'{st['address']}')")

        for r in st['restaurants']:
            restaurant_name = r['name'].replace("'", "''")
            restaurant_address = st['address'] if r['address'] == "Not provided" else r['address']
            restaurant_values.append(f"('{st['name']}', '{restaurant_name}', "
                                     f"ST_GeogFromText('SRID=4326;POINT({r['lon']} {r['lat']})'), "
                                     f"ARRAY[{', '.join(repr(c) for c in r['cuisine'])}], "
                                     f"'{restaurant_address}')")

with open('inserts', 'a', encoding='utf-8') as file:
    station_insert = f"""
INSERT INTO stations (name, location, address)
VALUES {',\n'.join(station_values)};"""

    restaurant_insert = f"""
INSERT INTO restaurants (station_id, name, location, cuisines, address)
SELECT s.station_id, d.name, d.location, d.cuisines, d.address
FROM (
  VALUES
    {',\n'.join(restaurant_values)}
) AS d(station_name, name, location, cuisines, address)
JOIN stations AS s
ON s.name = d.station_name;"""

    file.write(station_insert)
    file.write('\n\n')
    file.write(restaurant_insert)
