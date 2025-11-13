import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SmartWaterUsageData')

def lambda_handler(event, context):
    for record in event['Records']:
        data = json.loads(record['body'])
        table.put_item(
            Item={
                'device_id': data['device_id'],
                'timestamp': data['timestamp'],
                'flow_rate_lpm': Decimal(str(data['flow_rate_lpm']))
            }
        )
    return {
        'statusCode': 200,
        'body': 'Data inserted successfully!'
    }
