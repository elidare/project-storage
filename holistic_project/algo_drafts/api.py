# pip install openrouteservice shapely geopandas
# pip install dotenv


from shapely.geometry import LineString
from shapely.geometry import mapping  # for visualizations
from dotenv import load_dotenv
from constants import BUFFERED_ZONE, MINIMUM_SOC_AT_ARRIVAL, MAX_POWER, TEMP
from model_api import get_estimate_charging_time
import openrouteservice
import geopandas as gpd
import folium  # for visualizations
import json
import os

load_dotenv()
client = openrouteservice.Client(key=os.getenv('OPEN_ROUTE_SERVICE_API_KEY'))
# https://account.heigit.org/manage/key


def get_driving_etas(current_location, stations):
    # Prepare coordinates for the API
    locations = [current_location] + [tuple(l['coords']) for l in stations]

    # Call ORS Matrix API (driving duration in seconds)
    matrix = client.distance_matrix(
        locations=locations,
        profile='driving-car',
        metrics=['duration', 'distance'],
        units='km',
        sources=[0],  # only from current_location
        destinations=list(range(1, len(stations) + 1))
    )

    durations = matrix['durations'][0]
    distances = matrix['distances'][0]

    for i, r in enumerate(stations):
        r['travel_time_sec'] = durations[i]
        r['travel_time_min'] = round(durations[i] / 60, 1)
        r['distance_km'] = round(distances[i], 2)

    return stations


# Get location range
def get_location_range(current_location, destination):
    # source: (lon, lat) !
    # destination: (lon, lat) !
    coords = [current_location, destination]

    # Request the route geometry
    route = client.directions(
        coordinates=coords,
        profile='driving-car',
        format='geojson'
    )

    # Extract coordinates of the route (as (lon, lat))
    route_coords = route['features'][0]['geometry']['coordinates']

    # 3Convert route to a LineString
    line = LineString(route_coords)

    # Create a buffer (0.5 km = 500 m)
    # ORS coordinates are in lon/lat, so first project to metric (meters) CRS
    gdf = gpd.GeoDataFrame(geometry=[line], crs="EPSG:4326")
    gdf = gdf.to_crs(epsg=3857)  # Web Mercator, in meters

    buffered = gdf.buffer(BUFFERED_ZONE)  # 500 m each side → 1 km total width

    # 5Convert back to lat/lon if needed
    buffered = gpd.GeoDataFrame(geometry=buffered, crs="EPSG:3857").to_crs(epsg=4326)

    # Print bounding box (min_lon, min_lat, max_lon, max_lat)
    print(buffered.total_bounds)

    # -------- Optional: visualize
    # Convert shapely polygon to GeoJSON-like dict
    geojson_data = mapping(buffered.geometry.iloc[0])

    # Create map centered at midpoint
    m = folium.Map(location=[current_location[1] - current_location[0], destination[1] - destination[0]], zoom_start=14)

    # Add buffer polygon
    folium.GeoJson(geojson_data, name="Route Buffer").add_to(m)

    # Save or show
    m.save("route_buffer.html")
    print("Saved interactive map to route_buffer.html")


# Get stations, chargers, and restaurants from the database
def get_chargers_and_restaurants(location_range, connector_type, cuisines):
    # https://chatgpt.com/share/68f9048e-6d54-8003-9cb1-22ef67ffacaa - how to filter stations
    pass


# Get ETA for the returned restaurants
def get_charging_etas(current_location, stations, ev_model, current_car_range, current_soc, desired_soc):
    # ETA for driving from current_location to each station
    # stations_with_eta = get_driving_etas(current_location, stations)

    stations_with_eta_ = [{'name': 'Feast-faster 1 Pakila Helsinki', 'address': 'Pakilantie 61, Helsinki',
      'type': 'CCS (3), CHAdeMO (1), Type 2 (4)', 'max_op_power': '80 kW', 'lat': 60.2397157, 'lon': 24.9291792,
      'coords': [24.9291792, 60.2397157], 'restaurants': [
            {'name': 'House of Sandwiches', 'lat': 60.2383083, 'lon': 24.9278122, 'address': 'Pakilantie 56, Helsinki',
             'cuisine': 'Unknown', 'coords': [24.9278122, 60.2383083]}], 'travel_time_sec': 4026.08,
      'travel_time_min': 67.1, 'distance_km': 102.13},
     {'name': 'Feast-faster 8 Alepa Backas Vantaa', 'address': 'Ylästöntie 28, Vantaa', 'type': 'CCS (2), Type 2 (2)',
      'max_op_power': '80 kW', 'lat': 60.2850047, 'lon': 24.9526783, 'coords': [24.9526783, 60.2850047],
      'restaurants': [{'name': 'Backaksen kartano kesäravintola', 'lat': 60.2841155, 'lon': 24.9528945,
                       'address': 'Ylästöntie 28, Vantaa', 'cuisine': 'regional', 'coords': [24.9528945, 60.2841155]},
                      {'name': 'Star Lunch', 'lat': 60.2888129, 'lon': 24.9522375, 'address': 'Elannontie 5, Vantaa',
                       'cuisine': 'lunch', 'coords': [24.9522375, 60.2888129]}], 'travel_time_sec': 4258.21,
      'travel_time_min': 71.0, 'distance_km': 99.51},
     {'name': 'Feast-faster 217 Veturi', 'address': 'Tervasharjunkatu 1, Kouvola', 'type': 'CCS (4), Type 2 (4)',
      'max_op_power': '200 kW', 'lat': 60.876716, 'lon': 26.6512923, 'coords': [26.6512923, 60.876716], 'restaurants': [
         {'name': 'Fu Lam', 'lat': 60.8761602, 'lon': 26.6518056, 'address': 'Not provided', 'cuisine': 'chinese',
          'coords': [26.6518056, 60.8761602]},
         {'name': 'Mario', 'lat': 60.8762095, 'lon': 26.6522909, 'address': 'Not provided', 'cuisine': 'italian',
          'coords': [26.6522909, 60.8762095]},
         {'name': 'Teppanyaki Inn', 'lat': 60.876748, 'lon': 26.6523134, 'address': 'Not provided',
          'cuisine': 'Unknown', 'coords': [26.6523134, 60.876748]},
         {'name': 'Ristorante Momento', 'lat': 60.8770595, 'lon': 26.6521821, 'address': 'Not provided',
          'cuisine': 'Unknown', 'coords': [26.6521821, 60.8770595]}], 'travel_time_sec': 3398.34,
      'travel_time_min': 56.6, 'distance_km': 59.38}]

    available_stations = []

    # Calculate SoC decrease rate
    soc_rate = current_soc / current_car_range  # % decrease by 1 km

    for st in stations_with_eta_:
        # Calculate SoC at arrival
        soc_at_arrival = round(current_soc - soc_rate * st['distance_km'], 2)

        # If soc_at_arrival is less than minimum, continue MINIMUM_SOC_AT_ARRIVAL
        if soc_at_arrival < MINIMUM_SOC_AT_ARRIVAL:
            continue

        st['soc_at_arrival'] = soc_at_arrival

        # Calculate charging estimate
        soc_diff = desired_soc - soc_at_arrival
        estimate_charging_time = round(get_estimate_charging_time(ev_model, current_soc, soc_diff, MAX_POWER, TEMP), 2)

        st['estimate_charging_time_sec'] = estimate_charging_time
        st['estimate_charging_time_min'] = round(estimate_charging_time / 60, 1)
        print(st['estimate_charging_time_sec'], st['estimate_charging_time_min'])
        available_stations.append(st)

    print(available_stations)


# get_location_range((25.6589235, 60.9777510), (23.773557, 61.475202))
# 60.97775101669655, 25.658923522514566 - Lahti (25.6589235, 60.9777510)
# 61.475202787576556, 23.77355709300215 - Tampere (23.773557, 61.475202)

current_location = (25.6589235, 60.9777510)

###
with open('mock_data/stations_restaurants_initial.json', 'r', encoding='utf-8') as data:
    stations = json.load(data)

    # mock
station_list = [stations[0], stations[7], stations[216]]

get_charging_etas(current_location, station_list, "Skoda Enyaq iV", 105, 60, 80)

result = [
    {
        'name': 'Feast-faster 8 Alepa Backas Vantaa',
        'address': 'Ylästöntie 28, Vantaa',
        'type': 'CCS (2), Type 2 (2)',
        'max_op_power': '80 kW',
        'lat': 60.2850047, 'lon': 24.9526783,
        'coords': [24.9526783, 60.2850047],
        'restaurants': [{'name': 'Backaksen kartano kesäravintola', 'lat': 60.2841155, 'lon': 24.9528945, 'address': 'Ylästöntie 28, Vantaa', 'cuisine': 'regional', 'coords': [24.9528945, 60.2841155]}, {'name': 'Star Lunch', 'lat': 60.2888129, 'lon': 24.9522375, 'address': 'Elannontie 5, Vantaa', 'cuisine': 'lunch', 'coords': [24.9522375, 60.2888129]}],
        'travel_time_sec': 4258.21,
        'travel_time_min': 71.0,
        'distance_km': 99.51,
        'soc_at_arrival': 3.14,
        'estimate_charging_time_sec': 4307.07,
        'estimate_charging_time_min': 71.8
    }, {
        'name': 'Feast-faster 217 Veturi',
        'address': 'Tervasharjunkatu 1, Kouvola',
        'type': 'CCS (4), Type 2 (4)',
        'max_op_power': '200 kW',
        'lat': 60.876716, 'lon': 26.6512923,
        'coords': [26.6512923, 60.876716],
        'restaurants': [{'name': 'Fu Lam', 'lat': 60.8761602, 'lon': 26.6518056, 'address': 'Not provided', 'cuisine': 'chinese', 'coords': [26.6518056, 60.8761602]}, {'name': 'Mario', 'lat': 60.8762095, 'lon': 26.6522909, 'address': 'Not provided', 'cuisine': 'italian', 'coords': [26.6522909, 60.8762095]}, {'name': 'Teppanyaki Inn', 'lat': 60.876748, 'lon': 26.6523134, 'address': 'Not provided', 'cuisine': 'Unknown', 'coords': [26.6523134, 60.876748]}, {'name': 'Ristorante Momento', 'lat': 60.8770595, 'lon': 26.6521821, 'address': 'Not provided', 'cuisine': 'Unknown', 'coords': [26.6521821, 60.8770595]}],
        'travel_time_sec': 3398.34,
        'travel_time_min': 56.6,
        'distance_km': 59.38,
        'soc_at_arrival': 26.07,
        'estimate_charging_time_sec': 3504.3,
        'estimate_charging_time_min': 58.4
    }
]
