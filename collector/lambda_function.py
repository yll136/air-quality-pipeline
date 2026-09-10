import json, os, boto3
from datetime import datetime, timezone
from collect import collect_measurements, collect_weather

s3 = boto3.client("s3")
BUCKET = os.environ["BUCKET"]

def _write(prefix, records, now):
    if not records:
        return None
    key = f"{prefix}/dt={now:%Y-%m-%d}/hour={now:%H}/{now:%Y%m%dT%H%M%S}.jsonl"
    body = "\n".join(json.dumps(r) for r in records)
    s3.put_object(Bucket=BUCKET, Key=key, Body=body.encode())
    return key

def lambda_handler(event, context):
    now = datetime.now(timezone.utc)
    m = collect_measurements()
    w = collect_weather()
    return {
        "measurements": len(m),
        "weather": len(w),
        "measure_key": _write("raw", m, now),
        "weather_key": _write("raw_weather", w, now),
    }