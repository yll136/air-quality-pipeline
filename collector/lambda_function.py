import json, os, boto3
from datetime import datetime, timezone
from collect import collect

s3 = boto3.client("s3")
BUCKET = os.environ["BUCKET"]

def lambda_handler(event, context):
    recs = collect()
    now = datetime.now(timezone.utc)
    key = f"raw/dt={now:%Y-%m-%d}/hour={now:%H}/{now:%Y%m%dT%H%M%S}.jsonl"
    body = "\n".join(json.dumps(r) for r in recs)
    s3.put_object(Bucket=BUCKET, Key=key, Body=body.encode())
    return {"records": len(recs), "key": key}