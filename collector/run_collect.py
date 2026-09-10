import json
from config import METROS, RADIUS_M, PROVIDER_AIRNOW, PARAMS
from discover import get_locations, find_sensors
from measure import fetch_hours

name, lat, lon = METROS[0]
sensors = find_sensors(get_locations(lat, lon, RADIUS_M, PROVIDER_AIRNOW), PARAMS)
first = sensors[0]
print("sensor:", first["parameter"], "at", first["location_name"])
rows = fetch_hours(first["sensor_id"])
print("hours returned:", len(rows))
print(json.dumps(rows[-1], indent=2))