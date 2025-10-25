"""
Lambda function for Cart API
Handles: GET /cart, POST /cart/items, PUT /cart/items/{id}, DELETE /cart/items/{id}
"""
import json
import boto3
import os
import jwt
from decimal import Decimal
from datetime import datetime

# AWS clients
endpoint_url = os.getenv('AWS_ENDPOINT_URL') or None
dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)
CARTS_TABLE = os.getenv('CARTS_TABLE', 'ekart-carts-dev')
PRODUCTS_TABLE = os.getenv('PRODUCTS_TABLE', 'ekart-products-dev')

def extract_user_from_token(event):
    """Extract user ID from JWT token"""
    try:
        # Get authorization header
        headers = event.get('headers', {})
        auth_header = headers.get('Authorization') or headers.get('authorization')
        
        if not auth_header:
            return None
        
        # Extract token from "Bearer <token>"
        parts = auth_header.split(' ')
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return None
        
        token = parts[1]
        
        # Decode token without verification (LocalStack doesn't have proper keys)
        # In production, you should verify the token signature
        decoded = jwt.decode(token, options={"verify_signature": False})
        
        # Extract user ID from sub claim
        user_id = decoded.get('sub') or decoded.get('username')
        return user_id
        
    except Exception as e:
        print(f"Token extraction error: {str(e)}")
        return None

def decimal_default(obj):
    """JSON serializer for Decimal objects"""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def cors_response(status_code, body):
    """Return response with CORS headers"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
        },
        'body': json.dumps(body, default=decimal_default)
    }

def get_cart(user_id):
    """Get user's cart"""
    try:
        table = dynamodb.Table(CARTS_TABLE)
        response = table.get_item(Key={'user_id': user_id})
        
        if 'Item' not in response:
            # Return empty cart
            return cors_response(200, {
                'user_id': user_id,
                'items': [],
                'total_amount': 0,
                'updated_at': datetime.utcnow().isoformat()
            })
        
        return cors_response(200, response['Item'])
    except Exception as e:
        print(f"Error getting cart: {e}")
        return cors_response(500, {'error': str(e)})

def add_to_cart(user_id, body):
    """Add item to cart"""
    try:
        product_id = body['product_id']
        quantity = int(body.get('quantity', 1))
        
        # Verify product exists and get price
        products_table = dynamodb.Table(PRODUCTS_TABLE)
        product_response = products_table.get_item(Key={'product_id': product_id})
        
        if 'Item' not in product_response:
            return cors_response(404, {'error': 'Product not found'})
        
        product = product_response['Item']
        
        # Get or create cart
        carts_table = dynamodb.Table(CARTS_TABLE)
        cart_response = carts_table.get_item(Key={'user_id': user_id})
        
        if 'Item' in cart_response:
            cart = cart_response['Item']
            items = cart.get('items', [])
        else:
            cart = {'user_id': user_id, 'items': []}
            items = []
        
        # Check if product already in cart
        existing_item = None
        for item in items:
            if item['product_id'] == product_id:
                existing_item = item
                break
        
        if existing_item:
            existing_item['quantity'] = existing_item['quantity'] + quantity
        else:
            items.append({
                'product_id': product_id,
                'product_name': product.get('title', product.get('name', 'Unknown Product')),
                'price': product['price'],
                'quantity': quantity,
                'seller_id': product['seller_id']
            })
        
        # Calculate total
        total_amount = sum(Decimal(str(item['price'])) * item['quantity'] for item in items)
        
        # Update cart
        cart['items'] = items
        cart['total_amount'] = total_amount
        cart['updated_at'] = datetime.utcnow().isoformat()
        
        carts_table.put_item(Item=cart)
        
        return cors_response(200, cart)
    except Exception as e:
        print(f"Error adding to cart: {e}")
        return cors_response(500, {'error': str(e)})

def update_cart_item(user_id, product_id, query_params):
    """Update cart item quantity"""
    try:
        quantity = int(query_params.get('quantity', 1))
        
        # Get cart
        table = dynamodb.Table(CARTS_TABLE)
        response = table.get_item(Key={'user_id': user_id})
        
        if 'Item' not in response:
            return cors_response(404, {'error': 'Cart not found'})
        
        cart = response['Item']
        items = cart.get('items', [])
        
        # Find and update item
        found = False
        for item in items:
            if item['product_id'] == product_id:
                if quantity <= 0:
                    items.remove(item)
                else:
                    item['quantity'] = quantity
                found = True
                break
        
        if not found:
            return cors_response(404, {'error': 'Item not found in cart'})
        
        # Recalculate total
        total_amount = sum(Decimal(str(item['price'])) * item['quantity'] for item in items)
        
        cart['items'] = items
        cart['total_amount'] = total_amount
        cart['updated_at'] = datetime.utcnow().isoformat()
        
        table.put_item(Item=cart)
        
        return cors_response(200, cart)
    except Exception as e:
        print(f"Error updating cart: {e}")
        return cors_response(500, {'error': str(e)})

def remove_from_cart(user_id, product_id):
    """Remove item from cart"""
    try:
        table = dynamodb.Table(CARTS_TABLE)
        response = table.get_item(Key={'user_id': user_id})
        
        if 'Item' not in response:
            return cors_response(404, {'error': 'Cart not found'})
        
        cart = response['Item']
        items = cart.get('items', [])
        
        # Remove item
        items = [item for item in items if item['product_id'] != product_id]
        
        # Recalculate total
        total_amount = sum(Decimal(str(item['price'])) * item['quantity'] for item in items)
        
        cart['items'] = items
        cart['total_amount'] = total_amount
        cart['updated_at'] = datetime.utcnow().isoformat()
        
        table.put_item(Item=cart)
        
        return cors_response(200, {'message': 'Item removed from cart'})
    except Exception as e:
        print(f"Error removing from cart: {e}")
        return cors_response(500, {'error': str(e)})

def clear_cart(user_id):
    """Clear entire cart"""
    try:
        table = dynamodb.Table(CARTS_TABLE)
        table.delete_item(Key={'user_id': user_id})
        return cors_response(200, {'message': 'Cart cleared'})
    except Exception as e:
        print(f"Error clearing cart: {e}")
        return cors_response(500, {'error': str(e)})

def lambda_handler(event, context):
    """
    Main Lambda handler for Cart API
    """
    print(f"Event: {json.dumps(event)}")
    
    try:
        http_method = event.get('httpMethod', event.get('requestContext', {}).get('http', {}).get('method'))
        path = event.get('path', '')
        query_params = event.get('queryStringParameters') or {}
        
        # Handle OPTIONS for CORS
        if http_method == 'OPTIONS':
            return cors_response(200, {})
        
        # Extract user from JWT token
        user_id = extract_user_from_token(event)
        
        if not user_id:
            return cors_response(401, {'error': 'Authentication required'})
        
        # Parse path parameters
        path_params = event.get('pathParameters') or {}
        product_id = path_params.get('id') or path_params.get('product_id')
        
        # Parse body
        body = {}
        if event.get('body'):
            body = json.loads(event['body'])
        
        # Route to appropriate handler
        if http_method == 'GET' and '/items' not in path:
            return get_cart(user_id)
        
        elif http_method == 'POST' and '/items' in path:
            return add_to_cart(user_id, body)
        
        elif http_method == 'PUT' and product_id:
            return update_cart_item(user_id, product_id, query_params)
        
        elif http_method == 'DELETE' and product_id:
            return remove_from_cart(user_id, product_id)
        
        elif http_method == 'DELETE':
            return clear_cart(user_id)
        
        else:
            return cors_response(405, {'error': 'Method not allowed'})
            
    except Exception as e:
        print(f"Lambda handler error: {e}")
        return cors_response(500, {'error': str(e)})
