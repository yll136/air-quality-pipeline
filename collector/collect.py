import json, os
from config import METROS, RADIUS_M, PROVIDER_AIRNOW, PARAMS
from discover import get_locations, find_sensors
from measure import fetch_hours, to_record
from weather import fetch_weather

def collect_measurements():
    records = []
    for name, lat, lon in METROS:
        sensors = find_sensors(get_locations(lat, lon, RADIUS_M, PROVIDER_AIRNOW), PARAMS)
        for s in sensors:
            s["metro"] = name
            for hour in fetch_hours(s["sensor_id"]):
                records.append(to_record(s, hour))
    return records

def collect_weather():
    rows = []
    for name, lat, lon in METROS:
        rows.extend(fetch_weather(name, lat, lon))
    return rows