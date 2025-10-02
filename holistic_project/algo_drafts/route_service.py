import openrouteservice

# 1. Get an API key (free) from https://openrouteservice.org/sign-up/
# https://account.heigit.org/manage/key
with open('mock_data/openrouteservice_api_key', 'r') as f:
    API_KEY = f.readline().strip()  # DO NOT COMMIT API KEY, USE ENV or create an ignored file
client = openrouteservice.Client(key=API_KEY)


def find_closest(current_location, location_list):
    # 2. Prepare coordinates for the API
    locations = [current_location] + [tuple(l['coords']) for l in location_list]

    # 3. Call ORS Matrix API (driving duration in seconds)
    matrix = client.distance_matrix(
        locations=locations,
        profile='driving-car',
        metrics=['duration'],
        sources=[0],  # only from current_location
        destinations=list(range(1, len(location_list) + 1))
    )

    durations = matrix['durations'][0]

    # 4. Attach travel times back to restaurants
    for i, r in enumerate(location_list):
        r['travel_time_sec'] = durations[i]
        r['travel_time_min'] = round(durations[i] / 60, 1)

    # 5. Find the fastest one
    return min(location_list, key=lambda r: r['travel_time_sec'])
