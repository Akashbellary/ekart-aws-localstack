#!/usr/bin/env python3
"""
Seed database with sample data for development
"""
import boto3
import uuid
from datetime import datetime, timezone
from decimal import Decimal

# LocalStack configuration
LOCALSTACK_ENDPOINT = "http://localhost:4566"
AWS_REGION = "us-east-1"
ENV = "dev"

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=LOCALSTACK_ENDPOINT,
    region_name=AWS_REGION,
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

def seed_users():
    """Seed sample users"""
    table = dynamodb.Table(f'ekart-users-{ENV}')
    
    users = [
        {
            'user_id': str(uuid.uuid4()),
            'email': 'buyer@example.com',
            'full_name': 'John Buyer',
            'user_type': 'buyer',
            'is_verified': True,
            'seller_verified': False,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'updated_at': datetime.now(timezone.utc).isoformat()
        },
        {
            'user_id': str(uuid.uuid4()),
            'email': 'seller@example.com',
            'full_name': 'Jane Seller',
            'user_type': 'seller',
            'is_verified': True,
            'seller_verified': True,
            'business_name': 'Jane\'s Store',
            'created_at': datetime.now(timezone.utc).isoformat(),
            'updated_at': datetime.now(timezone.utc).isoformat()
        }
    ]
    
    for user in users:
        table.put_item(Item=user)
    
    print(f"✓ Seeded {len(users)} users")

def seed_products():
    """Seed sample products"""
    table = dynamodb.Table(f'ekart-products-{ENV}')
    
    products = [
        {
            'product_id': str(uuid.uuid4()),
            'seller_id': 'seller-123',
            'title': 'Wireless Bluetooth Headphones',
            'description': 'High-quality wireless headphones with noise cancellation',
            'category': 'electronics',
            'price': Decimal('79.99'),
            'currency': 'USD',
            'stock_quantity': 50,
            'is_active': True,
            'rating': Decimal('4.5'),
            'review_count': 120,
            'images': [],
            'variants': [],
            'tags': ['electronics', 'audio', 'wireless'],
            'brand': 'TechBrand',
            'created_at': datetime.now(timezone.utc).isoformat(),
            'updated_at': datetime.now(timezone.utc).isoformat()
        },
        {
            'product_id': str(uuid.uuid4()),
            'seller_id': 'seller-123',
            'title': 'Comfortable Running Shoes',
            'description': 'Lightweight and breathable running shoes',
            'category': 'sports',
            'price': Decimal('59.99'),
            'currency': 'USD',
            'stock_quantity': 100,
            'is_active': True,
            'rating': Decimal('4.7'),
            'review_count': 85,
            'images': [],
            'variants': [],
            'tags': ['sports', 'shoes', 'running'],
            'brand': 'SportsBrand',
            'created_at': datetime.now(timezone.utc).isoformat(),
            'updated_at': datetime.now(timezone.utc).isoformat()
        }
    ]
    
    for product in products:
        table.put_item(Item=product)
    
    print(f"✓ Seeded {len(products)} products")

if __name__ == "__main__":
    print("🌱 Seeding database with sample data...")
    try:
        seed_users()
        seed_products()
        print("✅ Database seeding completed successfully!")
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        exit(1)
