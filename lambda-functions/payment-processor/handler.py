import json
import boto3
import os

def lambda_handler(event, context):
    """
    Process payments for orders
    """
    print(f"Payment processor invoked with event: {json.dumps(event)}")
    
    try:
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Payment processed successfully'})
        }
    except Exception as e:
        print(f"Error processing payment: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
