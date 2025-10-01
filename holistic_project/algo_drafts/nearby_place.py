import openrouteservice
import json


# 1. Get an API key (free) from https://openrouteservice.org/sign-up/
# https://account.heigit.org/manage/key
with open('mock_data/openrouteservice_api_key', 'r') as f:
    API_KEY = f.readline().strip()  # DO NOT COMMIT API KEY, USE ENV or create an ignored file
client = openrouteservice.Client(key=API_KEY)
#
# # Your current location (lat, lon)
current_location = (25.7769, 61.0518)  # (lon, lat format!)

# Example locations (chargers)
with open('mock_data/chargers.json', 'r', encoding='utf-8') as f:
    chargers = json.load(f)
    

# with open('mock_data/restaurants.json', 'r', encoding='utf-8') as f:
#     restaurants = json.load(f)


# 2. Prepare coordinates for the API
locations = [current_location] + [tuple(c['coords']) for c in chargers]

# 3. Call ORS Matrix API (driving duration in seconds)
matrix = client.distance_matrix(
    locations=locations,
    profile='driving-car',
    metrics=['duration'],
    sources=[0],  # only from current_location
    destinations=list(range(1, len(chargers) + 1))
)

durations = matrix['durations'][0]

# 4. Attach travel times back to restaurants
for i, r in enumerate(chargers):
    r['travel_time_sec'] = durations[i]
    r['travel_time_min'] = round(durations[i] / 60, 1)

# 5. Find the fastest one
fastest = min(chargers, key=lambda r: r['travel_time_sec'])

print(fastest)

print(f'Fastest charger: {fastest['name']}')
print(f'Driving time: {fastest['travel_time_min']} minutes')

