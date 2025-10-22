from route_service import find_closest
import json


current_location = (25.536955291143588, 60.987465200776235)  # (lon, lat format!)


# Example locations (chargers)
with open('mock_data/chargers.json', 'r', encoding='utf-8') as f:
    chargers = json.load(f)


closest_charger = find_closest(current_location, chargers)  # each charger shall have 'coords' with (lon, lat) tuple

closest_charger_location = tuple(closest_charger['coords'])

print('Closest charger:', closest_charger)

