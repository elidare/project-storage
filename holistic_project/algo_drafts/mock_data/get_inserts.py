import json


station_values = []
restaurant_values = []

with open('stations_restaurants_fixed_cuisines.json', 'r', encoding='utf-8') as stations:
    stations = json.load(stations)
    for st in stations:
        if 'Espoo' in st['address'] or 'Helsinki' in st['address']:  # TEMP for testing, delete this if for all the data
            station_values.append(f"('{st['name']}', ST_GeogFromText('SRID=4326;POINT({st['lon']} {st['lat']})'))")

            for r in st['restaurants']:
                restaurant_name = r['name'].replace("'", "''")
                restaurant_values.append(f"('{st['name']}', '{restaurant_name}', "
                                         f"ST_GeogFromText('SRID=4326;POINT({r['lon']} {st['lat']})'), "
                                         f"ARRAY[{', '.join(repr(c) for c in r['cuisine'])}])")

with open('inserts', 'a', encoding='utf-8') as file:
    station_insert = f"""
INSERT INTO stations (name, location)
VALUES {',\n'.join(station_values)};"""

    restaurant_insert = f"""
INSERT INTO restaurants (station_id, name, location, cuisines)
SELECT s.station_id, d.name, d.location, d.cuisines
FROM (
  VALUES
    {',\n'.join(restaurant_values)}
) AS d(station_name, name, location, cuisines)
JOIN stations AS s
ON s.name = d.station_name;"""

    file.write(station_insert)
    file.write('\n\n')
    file.write(restaurant_insert)
