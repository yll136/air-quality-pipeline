from config import METROS, RADIUS_M, PROVIDER_AIRNOW, PARAMS
from discover import get_locations, find_sensors

for name, lat, lon in METROS:
    locs = get_locations(lat, lon, RADIUS_M, PROVIDER_AIRNOW)
    sensors = find_sensors(locs, PARAMS)
    print(f"{name}: {len(sensors)} live sensors")