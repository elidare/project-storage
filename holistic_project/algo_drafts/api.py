# pip install openrouteservice shapely geopandas
# pip install dotenv


from shapely.geometry import LineString
from shapely.geometry import mapping  # for visualizations
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import openrouteservice
import geopandas as gpd
import folium  # for visualizations
import json
import os


load_dotenv()
client = openrouteservice.Client(key=os.getenv('OPEN_ROUTE_SERVICE_API_KEY'))
# https://account.heigit.org/manage/key
BUFFERED_ZONE = 1000  # m


# Get location range
def get_location_range(source, destination):
    # source: (lon, lat) !
    # destination: (lon, lat) !
    coords = [
        source,
        destination
    ]

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

    # Optional: visualize
    # Convert shapely polygon to GeoJSON-like dict
    geojson_data = mapping(buffered.geometry.iloc[0])

    # Create map centered at midpoint
    m = folium.Map(location=[source[1] - source[0], destination[1] - destination[0]], zoom_start=14)

    # Add buffer polygon
    folium.GeoJson(geojson_data, name="Route Buffer").add_to(m)

    # Save or show
    m.save("route_buffer.html")
    print("Saved interactive map to route_buffer.html")

# https://chatgpt.com/share/68f9048e-6d54-8003-9cb1-22ef67ffacaa

# Get stations, chargers, and restaurants from the database
def get_chargers_and_restaurants(location_range, connector_type, cuisines):
    pass


# Get ETA for the returned restaurants
def get_charging_etas(stations, ev_model, current_car_range, current_soc, desired_soc):
    pass


get_location_range((25.6589235, 60.9777510), (23.773557, 61.475202))
# 60.97775101669655, 25.658923522514566 - Lahti (25.6589235, 60.9777510)
# 61.475202787576556, 23.77355709300215 - Tampere (23.773557, 61.475202)
