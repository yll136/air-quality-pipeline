import os
from datetime import datetime, timezone, timedelta
from net import make_session

BASE = "https://api.openaq.org/v3"
SESSION = make_session()

def get_locations(lat, lon, radius, provider):
    headers = {"X-API-Key": os.environ["OPENAQ_KEY"]}
    params = {
        "coordinates": f"{lat},{lon}",
        "radius": radius,
        "providers_id": provider,
        "limit": 100,
    }
    r = SESSION.get(f"{BASE}/locations", headers=headers, params=params)
    r.raise_for_status()
    return r.json()["results"]

def _is_live(loc, max_age_hours=48):
    dt = loc.get("datetimeLast")
    if not dt:
        return False
    last = datetime.fromisoformat(dt["utc"].replace("Z", "+00:00"))
    return datetime.now(timezone.utc) - last < timedelta(hours=max_age_hours)

def find_sensors(locations, wanted_params):
    out = []
    for loc in locations:
        if not _is_live(loc):
            continue
        for s in loc["sensors"]:
            if s["parameter"]["name"] in wanted_params:
                out.append({
                    "sensor_id": s["id"],
                    "parameter": s["parameter"]["name"],
                    "location_id": loc["id"],
                    "location_name": loc["name"],
                    "lat": loc["coordinates"]["latitude"],
                    "lon": loc["coordinates"]["longitude"],
                })
    return out