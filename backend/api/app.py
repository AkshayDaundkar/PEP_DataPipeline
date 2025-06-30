from fastapi import FastAPI, Query, HTTPException, Request
from typing import Optional
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import json
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from data.simulate_data import generate_data, upload_to_s3, SITE_IDS

# Logging setup
logging.basicConfig(level=logging.INFO)

S3_BUCKET_NAME = "renewable-energy-pipeline-akshay"
s3 = boto3.client("s3")
dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table("energy_data")

app = FastAPI(title="Energy Data API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper: convert Decimal → float
def clean_record(record):
    for k, v in record.items():
        if isinstance(v, Decimal):
            record[k] = float(v)
    return record

@app.get("/records")
def get_records(
    site_id: str,
    last_key: Optional[str] = None,
    limit: int = 100
):
    """Get records for a site with pagination."""
    query_kwargs = {
        "KeyConditionExpression": Key("site_id").eq(site_id),
        "Limit": limit
    }
    if last_key:
        query_kwargs["ExclusiveStartKey"] = json.loads(last_key)
    response = table.query(**query_kwargs)
    items = response.get("Items", [])
    last_evaluated_key = response.get("LastEvaluatedKey")
    return {
        "records": [clean_record(i) for i in items],
        "last_key": json.dumps(last_evaluated_key) if last_evaluated_key else None
    }

@app.get("/anomalies/{site_id}")
def get_anomalies(
    site_id: str,
    last_key: Optional[str] = None,
    limit: int = 100
):
    """Get anomaly records for a site with pagination."""
    query_kwargs = {
        "KeyConditionExpression": Key("site_id").eq(site_id),
        "Limit": limit
    }
    if last_key:
        query_kwargs["ExclusiveStartKey"] = json.loads(last_key)
    response = table.query(**query_kwargs)
    items = response.get("Items", [])
    anomalies = [clean_record(i) for i in items if i.get("anomaly") == True]
    last_evaluated_key = response.get("LastEvaluatedKey")
    return {
        "anomalies": anomalies,
        "last_key": json.dumps(last_evaluated_key) if last_evaluated_key else None
    }

@app.post("/simulatedata")
def simulate_one_batch(
    batch_size: int = 1,
    sites: Optional[str] = None
):
    """Trigger a new batch of simulated data and upload to S3."""
    try:
        if sites:
            site_ids = sites.split(",")
        else:
            site_ids = SITE_IDS
        data = generate_data(batch_size=batch_size, site_ids=site_ids)
        filename = upload_to_s3(data)
        logging.info(f"Simulated data uploaded as {filename}")
        return {"status": "success", "filename": filename}
    except Exception as e:
        logging.error(f"Simulation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
#"""Fetch the content of a specific file from S3."""
@app.get("/file/{filename}")
def get_file_content(filename: str):
    try:
        obj = s3.get_object(Bucket=S3_BUCKET_NAME, Key=filename)
        content = obj["Body"].read().decode("utf-8")
        return JSONResponse(content=json.loads(content))
    except s3.exceptions.NoSuchKey:
        logging.error(f"File not found: {filename}")
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        logging.error(f"Error fetching file {filename}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/all-records")
def get_all_records(limit: int = 100):
    scan = table.scan(Limit = limit)
    items = scan.get("Items", [])
    return {"records": [clean_record(i) for i in items]}
