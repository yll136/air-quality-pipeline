import json, os
from config import METROS, RADIUS_M, PROVIDER_AIRNOW, PARAMS
from discover import get_locations, find_sensors
from measure import fetch_hours, to_record

def collect():
    records = []
    for name, lat, lon in METROS:
        sensors = find_sensors(get_locations(lat, lon, RADIUS_M, PROVIDER_AIRNOW), PARAMS)
        for s in sensors:
            for hour in fetch_hours(s["sensor_id"]):
                records.append(to_record(s, hour))
        print(f"{name}: collected")
    return records

if __name__ == "__main__":
    recs = collect()
    os.makedirs("out", exist_ok=True)
    with open("out/sample.jsonl", "w") as f:
        for r in recs:
            f.write(json.dumps(r) + "\n")
    print("total records:", len(recs))