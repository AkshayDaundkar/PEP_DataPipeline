import json
import random
import time
from datetime import datetime, timezone
import boto3
import logging
import argparse
import os
logging.basicConfig(level=logging.INFO)



# AWS S3 setup
S3_BUCKET_NAME = "renewable-energy-pipeline-akshay"  # change if needed
REGION = "us-east-1"

# Simulated site IDs
SITE_IDS = ["site_alpha", "site_beta", "site_gamma", "site_delta"]

# Initialize boto3 S3 client
s3 = boto3.client("s3", region_name=REGION)

def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=int, default=int(os.getenv("SIM_INTERVAL", 120)), help="Interval in seconds")
    parser.add_argument("--batch_size", type=int, default=int(os.getenv("BATCH_SIZE", 1)), help="Records per site per batch")
    parser.add_argument("--sites", type=str, default=",".join(SITE_IDS), help="Comma-separated site IDs")
    args = parser.parse_args()
    return args


def validate_entry(entry):
    required = ["site_id", "timestamp", "energy_generated_kwh", "energy_consumed_kwh"]
    return all(k in entry for k in required)


def generate_data(batch_size=1,site_ids=None):
    entries = []
    for _ in range(batch_size):
        for site_id in site_ids:
            entry = {
                "site_id": site_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "energy_generated_kwh": round(random.uniform(-10.0, 100.0), 2),
                "energy_consumed_kwh": round(random.uniform(0.0, 90.0), 2)
            }
            if validate_entry(entry):
                entries.append(entry)
    return entries

def upload_to_s3(data):
    try:
        filename = f"energy_data_{int(time.time())}.json"
        s3.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=filename,
            Body=json.dumps(data),
            ContentType='application/json'
        )
        print(f"[Uploaded] {filename} to bucket {S3_BUCKET_NAME}")
        logging.info(f"[Uploaded] {filename} to bucket {S3_BUCKET_NAME}")
        return filename 
    except Exception as e:
        logging.error(f"Failed to upload {filename}: {e}")
        return None

def main():
    args = get_config()
    site_ids = args.sites.split(",")

    print("Starting data simulation (Ctrl+C to stop)...")
    try:
        while True:
            data = generate_data(args.batch_size,site_ids)
            upload_to_s3(data)
            time.sleep(args.interval)  # Wait 2 minutes
    except KeyboardInterrupt:
        print("Simulation stopped.")

if __name__ == "__main__":
    main()
