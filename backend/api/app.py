from fastapi import FastAPI, Query
from typing import Optional, List
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
import os
from fastapi import HTTPException
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from data.simulate_data import generate_data, upload_to_s3
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import time
from fastapi import Request, HTTPException

LAST_SIMULATION_TIME = {}


S3_BUCKET_NAME = "renewable-energy-pipeline-akshay"
s3 = boto3.client("s3")

app = FastAPI(title="Energy Data API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
def get_records(site_id: str):
    from boto3.dynamodb.conditions import Key
    response = table.query(KeyConditionExpression=Key("site_id").eq(site_id))
    items = response.get("Items", [])
    return {"records": [clean_record(i) for i in items]}

@app.get("/anomalies/{site_id}")
def get_anomalies(site_id: str):
    response = table.query(
        KeyConditionExpression=Key("site_id").eq(site_id)
    )
    items = response.get("Items", [])
    anomalies = [clean_record(i) for i in items if i.get("anomaly") == True]
    return {"anomalies": anomalies}



@app.post("/simulatedata")
def simulate_one_batch():
    try:
        data = generate_data()
        filename = upload_to_s3(data)
        return {"status": "success", "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/file/{filename}")
def get_file_content(filename: str):
    try:
        obj = s3.get_object(Bucket=S3_BUCKET_NAME, Key=filename)
        content = obj["Body"].read().decode("utf-8")
        return JSONResponse(content=json.loads(content))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/all-records")
def get_all_records():
    scan = table.scan()
    items = scan.get("Items", [])
    return {"records": [clean_record(i) for i in items]}
