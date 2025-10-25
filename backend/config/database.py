import os
import boto3
from typing import Optional

# Get LocalStack endpoint from environment
LOCALSTACK_ENDPOINT = os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
ENV = os.getenv("ENV", "dev")

# Initialize AWS clients for LocalStack
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=LOCALSTACK_ENDPOINT,
    region_name=AWS_REGION,
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

s3_client = boto3.client(
    's3',
    endpoint_url=LOCALSTACK_ENDPOINT,
    region_name=AWS_REGION,
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

cognito_client = boto3.client(
    'cognito-idp',
    endpoint_url=LOCALSTACK_ENDPOINT,
    region_name=AWS_REGION,
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

# Table names
USERS_TABLE = f"ekart-users-{ENV}"
PRODUCTS_TABLE = f"ekart-products-{ENV}"
ORDERS_TABLE = f"ekart-orders-{ENV}"
CARTS_TABLE = f"ekart-carts-{ENV}"
INVENTORY_TABLE = f"ekart-inventory-{ENV}"

async def init_db():
    """Initialize database connections"""
    print(f"Initializing database connections for environment: {ENV}")
    print(f"Using LocalStack endpoint: {LOCALSTACK_ENDPOINT}")
    return True
