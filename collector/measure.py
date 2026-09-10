import os, time
from datetime import datetime, timezone, timedelta
from net import make_session

BASE = "https://api.openaq.org/v3"
SESSION = make_session()

def fetch_hours(sensor_id, hours_back=6):
    time.sleep(1.1)   # stay under 60 requests/min
    headers = {"X-API-Key": os.environ["OPENAQ_KEY"]}
    start = datetime.now(timezone.utc) - timedelta(hours=hours_back)
    params = {
        "datetime_from": start.strftime("%Y-%m-%dT%H:00:00Z"),
        "limit": 100,
    }
    url = f"{BASE}/sensors/{sensor_id}/hours"
    r = SESSION.get(url, headers=headers, params=params)
    r.raise_for_status()
    return r.json()["results"]

def to_record(sensor, hour):
    return {
        "metro":         sensor["metro"],
        "sensor_id":     sensor["sensor_id"],
        "location_id":   sensor["location_id"],
        "location_name": sensor["location_name"],
        "lat":           sensor["lat"],
        "lon":           sensor["lon"],
        "parameter":     hour["parameter"]["name"],
        "units":         hour["parameter"]["units"],
        "value":         hour["value"],
        "hour_utc":      hour["period"]["datetimeTo"]["utc"],
        "pct_complete":  hour["coverage"]["percentComplete"],
    }