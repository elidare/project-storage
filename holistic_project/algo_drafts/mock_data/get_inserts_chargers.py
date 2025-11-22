import json
import re


charger_values = []
pattern_chargers = r'^(.*?)\s*\((\d+)\)$'
MAX_CHARGERS_BY_TYPE = 2
MAX_CHARGERS_PER_STATION = 4


with open('stations_restaurants_shortened.json', 'r', encoding='utf-8') as stations:
    stations = json.load(stations)
    for st in stations:
        chargers = []
        chargers_initial = [c.strip() for c in st['type'].split(',')]
        for c in chargers_initial:
            match = re.match(pattern_chargers, c)
            if match:
                name = match.group(1).strip()
                number = int(match.group(2))
                max_power = int(st['max_op_power'].split()[0])
                power = 22 if name == 'Type 2' else max_power
                number = number if number <= MAX_CHARGERS_BY_TYPE else MAX_CHARGERS_BY_TYPE
                for _ in range(number):
                    if len(chargers) == MAX_CHARGERS_PER_STATION:
                        break
                    chargers.append({
                        "station_name": st['name'],
                        "connector_type": name,
                        "power": power
                    })
        st['chargers'] = chargers
        del st['type']
        del st['max_op_power']

with open('stations_restaurants_shortened_chargers.json', 'w', encoding='utf-8') as f:
    json.dump(stations, f, ensure_ascii=False, indent=4)

for st in stations:
    for ch in st['chargers']:
        charger_values.append(f"('{st['name']}', "
                              f"'{ch['connector_type']}', "
                              f"{ch['power']})")


with open('inserts_chargers', 'a', encoding='utf-8') as file:
    charger_insert = f"""
INSERT INTO chargers (station_id, connector_type, power)
SELECT
    s.station_id,
    c.connector_type::connector_type, 
    c.power
FROM (
  VALUES
    {',\n'.join(charger_values)}
) AS c(station_name, connector_type, power)
JOIN stations AS s
ON s.name = c.station_name;"""

    file.write(charger_insert)
