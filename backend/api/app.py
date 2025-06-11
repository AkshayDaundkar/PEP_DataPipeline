from fastapi import FastAPI, Query
from typing import Optional, List
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
import os
from fastapi import HTTPException


app = FastAPI(title="Energy Data API")

# AWS setup
dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table("energy_data")

# Helper: convert Decimal → float
def clean_record(record):
    for k, v in record.items():
        if isinstance(v, Decimal):
            record[k] = float(v)
    return record

@app.get("/records")
def get_records(
    site_id: str = Query(..., description="Site ID to filter"),
    start: Optional[str] = Query(None, description="Start timestamp (ISO 8601)"),
    end: Optional[str] = Query(None, description="End timestamp (ISO 8601)")
):
    key_expr = Key("site_id").eq(site_id)

    response = table.query(
        KeyConditionExpression=key_expr
    )

    records = [clean_record(r) for r in response.get("Items", [])]

    # Optional: filter by time range
    if start or end:
        def within_range(record):
            try:
                ts = datetime.fromisoformat(record["timestamp"])
                if start:
                    start_dt = datetime.fromisoformat(start)
                    if ts < start_dt:
                        return False
                if end:
                    end_dt = datetime.fromisoformat(end)
                    if ts > end_dt:
                        return False
                return True
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid timestamp format. Use ISO 8601 format like '2025-06-01T00:00:00'")
        return {"records": records}     


@app.get("/anomalies/{site_id}")
def get_anomalies(site_id: str):
    response = table.query(
        KeyConditionExpression=Key("site_id").eq(site_id)
    )
    items = response.get("Items", [])
    anomalies = [clean_record(i) for i in items if i.get("anomaly") == True]
    return {"anomalies": anomalies}
