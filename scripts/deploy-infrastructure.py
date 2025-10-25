#!/usr/bin/env python3
"""
Deploy AWS infrastructure to LocalStack using boto3 directly
This bypasses CloudFormation limitations in LocalStack
"""
import boto3
import time

# LocalStack configuration
ENDPOINT = "http://localhost:4566"
REGION = "us-east-1"
ENV = "dev"

def create_aws_clients():
    """Create AWS clients for LocalStack"""
    config = {
        'endpoint_url': ENDPOINT,
        'region_name': REGION,
        'aws_access_key_id': 'test',
        'aws_secret_access_key': 'test'
    }
    
    return {
        'dynamodb': boto3.client('dynamodb', **config),
        'cognito': boto3.client('cognito-idp', **config),
        's3': boto3.client('s3', **config)
    }

def create_dynamodb_tables(dynamodb):
    """Create DynamoDB tables"""
    print("📦 Creating DynamoDB tables...")
    
    tables = [
        {
            'TableName': f'ekart-users-{ENV}',
            'KeySchema': [{'AttributeName': 'user_id', 'KeyType': 'HASH'}],
            'AttributeDefinitions': [
                {'AttributeName': 'user_id', 'AttributeType': 'S'},
                {'AttributeName': 'email', 'AttributeType': 'S'}
            ],
            'GlobalSecondaryIndexes': [{
                'IndexName': 'email-index',
                'KeySchema': [{'AttributeName': 'email', 'KeyType': 'HASH'}],
                'Projection': {'ProjectionType': 'ALL'}
            }],
            'BillingMode': 'PAY_PER_REQUEST'
        },
        {
            'TableName': f'ekart-products-{ENV}',
            'KeySchema': [{'AttributeName': 'product_id', 'KeyType': 'HASH'}],
            'AttributeDefinitions': [
                {'AttributeName': 'product_id', 'AttributeType': 'S'},
                {'AttributeName': 'seller_id', 'AttributeType': 'S'},
                {'AttributeName': 'category', 'AttributeType': 'S'}
            ],
            'GlobalSecondaryIndexes': [
                {
                    'IndexName': 'seller-index',
                    'KeySchema': [{'AttributeName': 'seller_id', 'KeyType': 'HASH'}],
                    'Projection': {'ProjectionType': 'ALL'}
                },
                {
                    'IndexName': 'category-index',
                    'KeySchema': [{'AttributeName': 'category', 'KeyType': 'HASH'}],
                    'Projection': {'ProjectionType': 'ALL'}
                }
            ],
            'BillingMode': 'PAY_PER_REQUEST'
        },
        {
            'TableName': f'ekart-orders-{ENV}',
            'KeySchema': [{'AttributeName': 'order_id', 'KeyType': 'HASH'}],
            'AttributeDefinitions': [
                {'AttributeName': 'order_id', 'AttributeType': 'S'},
                {'AttributeName': 'buyer_id', 'AttributeType': 'S'},
                {'AttributeName': 'seller_id', 'AttributeType': 'S'}
            ],
            'GlobalSecondaryIndexes': [
                {
                    'IndexName': 'buyer-index',
                    'KeySchema': [{'AttributeName': 'buyer_id', 'KeyType': 'HASH'}],
                    'Projection': {'ProjectionType': 'ALL'}
                },
                {
                    'IndexName': 'seller-index',
                    'KeySchema': [{'AttributeName': 'seller_id', 'KeyType': 'HASH'}],
                    'Projection': {'ProjectionType': 'ALL'}
                }
            ],
            'BillingMode': 'PAY_PER_REQUEST'
        },
        {
            'TableName': f'ekart-carts-{ENV}',
            'KeySchema': [{'AttributeName': 'user_id', 'KeyType': 'HASH'}],
            'AttributeDefinitions': [{'AttributeName': 'user_id', 'AttributeType': 'S'}],
            'BillingMode': 'PAY_PER_REQUEST'
        },
        {
            'TableName': f'ekart-inventory-{ENV}',
            'KeySchema': [{'AttributeName': 'product_id', 'KeyType': 'HASH'}],
            'AttributeDefinitions': [{'AttributeName': 'product_id', 'AttributeType': 'S'}],
            'BillingMode': 'PAY_PER_REQUEST'
        }
    ]
    
    for table_config in tables:
        try:
            dynamodb.create_table(**table_config)
            print(f"  ✓ Created table: {table_config['TableName']}")
        except dynamodb.exceptions.ResourceInUseException:
            print(f"  ⚠ Table already exists: {table_config['TableName']}")
        except Exception as e:
            print(f"  ✗ Error creating table {table_config['TableName']}: {e}")

def create_cognito_user_pool(cognito):
    """Create Cognito user pool"""
    print("🔐 Creating Cognito user pool...")
    
    try:
        response = cognito.create_user_pool(
            PoolName=f'ekart-users-{ENV}',
            Policies={
                'PasswordPolicy': {
                    'MinimumLength': 8,
                    'RequireUppercase': True,
                    'RequireLowercase': True,
                    'RequireNumbers': True,
                    'RequireSymbols': False
                }
            },
            AutoVerifiedAttributes=['email']
        )
        user_pool_id = response['UserPool']['Id']
        print(f"  ✓ Created user pool: {user_pool_id}")
        
        # Create user pool client
        client_response = cognito.create_user_pool_client(
            UserPoolId=user_pool_id,
            ClientName=f'ekart-client-{ENV}',
            ExplicitAuthFlows=['ALLOW_USER_SRP_AUTH', 'ALLOW_REFRESH_TOKEN_AUTH']
        )
        print(f"  ✓ Created user pool client: {client_response['UserPoolClient']['ClientId']}")
        
        return user_pool_id
        
    except cognito.exceptions.ResourceConflictException:
        print(f"  ⚠ User pool already exists")
        # List existing pools to get ID
        pools = cognito.list_user_pools(MaxResults=10)
        for pool in pools.get('UserPools', []):
            if pool['Name'] == f'ekart-users-{ENV}':
                return pool['Id']
    except Exception as e:
        print(f"  ✗ Error creating user pool: {e}")
        return None

def create_s3_buckets(s3):
    """Create S3 buckets"""
    print("🪣 Creating S3 buckets...")
    
    buckets = [
        f'ekart-product-images-{ENV}'
    ]
    
    for bucket_name in buckets:
        try:
            s3.create_bucket(Bucket=bucket_name)
            print(f"  ✓ Created bucket: {bucket_name}")
        except s3.exceptions.BucketAlreadyOwnedByYou:
            print(f"  ⚠ Bucket already exists: {bucket_name}")
        except Exception as e:
            print(f"  ✗ Error creating bucket {bucket_name}: {e}")

def main():
    """Main deployment function"""
    print("🚀 Deploying EKart Store infrastructure to LocalStack...\n")
    
    try:
        # Create AWS clients
        clients = create_aws_clients()
        
        # Create resources
        create_dynamodb_tables(clients['dynamodb'])
        print()
        
        user_pool_id = create_cognito_user_pool(clients['cognito'])
        print()
        
        create_s3_buckets(clients['s3'])
        print()
        
        print("✅ Infrastructure deployment completed successfully!")
        print(f"\nUser Pool ID: {user_pool_id}")
        print(f"Region: {REGION}")
        print(f"Environment: {ENV}")
        
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        exit(1)

if __name__ == "__main__":
    main()
