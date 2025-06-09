import json
import random
import time
from datetime import datetime
import boto3

# AWS S3 setup
S3_BUCKET_NAME = "renewable-energy-pipeline-akshay"  # change if needed
REGION = "us-east-1"

# Simulated site IDs
SITE_IDS = ["site_alpha", "site_beta", "site_gamma", "site_delta"]

# Initialize boto3 S3 client
s3 = boto3.client("s3", region_name=REGION)

def generate_data():
    entries = []
    for site_id in SITE_IDS:
        entry = {
            "site_id": site_id,
            "timestamp": datetime.utcnow().isoformat(),
            "energy_generated_kwh": round(random.uniform(-10.0, 100.0), 2),
            "energy_consumed_kwh": round(random.uniform(0.0, 90.0), 2)
        }
        entries.append(entry)
    return entries

def upload_to_s3(data):
    filename = f"energy_data_{int(time.time())}.json"
    s3.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=filename,
        Body=json.dumps(data),
        ContentType='application/json'
    )
    print(f"[Uploaded] {filename} to bucket {S3_BUCKET_NAME}")

def main():
    print("Starting data simulation (Ctrl+C to stop)...")
    try:
        while True:
            data = generate_data()
            upload_to_s3(data)
            time.sleep(120)  # Wait 5 minutes
    except KeyboardInterrupt:
        print("Simulation stopped.")

if __name__ == "__main__":
    main()
