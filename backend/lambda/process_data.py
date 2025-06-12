import json
import boto3
import os
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    sns = boto3.client('sns')
    SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        file_key = record['s3']['object']['key']

        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        content = response['Body'].read()

        # Parse float fields as Decimal
        entries = json.loads(content, parse_float=Decimal)

        for entry in entries:
            site_id = entry['site_id']
            timestamp = entry['timestamp']
            gen = entry['energy_generated_kwh']
            con = entry['energy_consumed_kwh']
            net = gen - con
            anomaly = gen < 0 or con < 0

            table.put_item(Item={
                'site_id': site_id,
                'timestamp': timestamp,
                'energy_generated_kwh': gen,
                'energy_consumed_kwh': con,
                'net_energy_kwh': net,
                'anomaly': anomaly
            })
            
            if anomaly:
                message = (
                    f"Anomaly Detected!\n"
                    f"Site: {site_id}\n"
                    f"Timestamp: {timestamp}\n"
                    f"Generated: {gen}\n"
                    f"Consumed: {con}"
                )
                sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Subject="Energy Anomaly Alert",
                    Message=message
                )


    return {
        'statusCode': 200,
        'body': json.dumps('Processed successfully')
    }
