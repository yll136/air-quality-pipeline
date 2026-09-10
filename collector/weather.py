import time
from net import make_session

SESSION = make_session()
BASE = "https://api.open-meteo.com/v1/forecast"

def fetch_weather(metro, lat, lon):
    time.sleep(0.2)
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,wind_speed_10m,relative_humidity_2m",
        "past_days": 1,
        "forecast_days": 1,
    }
    r = SESSION.get(BASE, params=params)
    r.raise_for_status()
    h = r.json()["hourly"]
    out = []
    for i, t in enumerate(h["time"]):
        out.append({
            "metro": metro,
            "hour_utc": t,
            "temp_c": h["temperature_2m"][i],
            "wind_kmh": h["wind_speed_10m"][i],
            "humidity_pct": h["relative_humidity_2m"][i],
        })
    return out