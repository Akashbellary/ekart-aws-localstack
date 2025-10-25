from typing import Optional
from config.database import dynamodb, CARTS_TABLE
from datetime import datetime
from decimal import Decimal
import uuid

class CartService:
    def __init__(self):
        self.carts_table = dynamodb.Table(CARTS_TABLE)

    async def get_cart(self, user_id: str):
        """Get user's cart"""
        try:
            response = self.carts_table.get_item(Key={'user_id': user_id})
            if 'Item' in response:
                cart = response['Item']
                # Convert all Decimals to regular types for JSON serialization
                return self._convert_decimals(cart)
            else:
                # Return empty cart
                return {
                    'user_id': user_id,
                    'items': [],
                    'created_at': datetime.utcnow().isoformat(),
                    'updated_at': datetime.utcnow().isoformat()
                }
        except Exception as e:
            print(f"Error getting cart: {e}")
            return {
                'user_id': user_id,
                'items': []
            }

    async def add_item(self, user_id: str, product_id: str, quantity: int):
        """Add item to cart"""
        try:
            cart = await self.get_cart(user_id)
            
            # Check if item already exists
            existing_item = None
            for item in cart['items']:
                if item['product_id'] == product_id:
                    existing_item = item
                    break
            
            if existing_item:
                # Update quantity
                existing_item['quantity'] += quantity
            else:
                # Add new item
                cart['items'].append({
                    'product_id': product_id,
                    'quantity': quantity,
                    'added_at': datetime.utcnow().isoformat()
                })
            
            cart['updated_at'] = datetime.utcnow().isoformat()
            
            # Convert floats to Decimals for DynamoDB
            cart_for_db = self._prepare_for_dynamodb(cart)
            self.carts_table.put_item(Item=cart_for_db)
            
            return cart
        except Exception as e:
            print(f"Error adding to cart: {e}")
            raise

    async def remove_item(self, user_id: str, product_id: str):
        """Remove item from cart"""
        try:
            cart = await self.get_cart(user_id)
            cart['items'] = [item for item in cart['items'] if item['product_id'] != product_id]
            cart['updated_at'] = datetime.utcnow().isoformat()
            
            cart_for_db = self._prepare_for_dynamodb(cart)
            self.carts_table.put_item(Item=cart_for_db)
            
            return cart
        except Exception as e:
            print(f"Error removing from cart: {e}")
            raise

    async def update_quantity(self, user_id: str, product_id: str, quantity: int):
        """Update item quantity"""
        try:
            cart = await self.get_cart(user_id)
            
            for item in cart['items']:
                if item['product_id'] == product_id:
                    item['quantity'] = quantity
                    break
            
            cart['updated_at'] = datetime.utcnow().isoformat()
            
            cart_for_db = self._prepare_for_dynamodb(cart)
            self.carts_table.put_item(Item=cart_for_db)
            
            return cart
        except Exception as e:
            print(f"Error updating cart quantity: {e}")
            raise

    def _convert_decimals(self, obj):
        """Convert Decimal to float for JSON serialization"""
        if isinstance(obj, dict):
            return {k: self._convert_decimals(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_decimals(item) for item in obj]
        elif isinstance(obj, Decimal):
            return float(obj)
        return obj

    def _prepare_for_dynamodb(self, obj):
        """Prepare data for DynamoDB by converting all floats to Decimals"""
        if isinstance(obj, dict):
            return {k: self._prepare_for_dynamodb(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._prepare_for_dynamodb(item) for item in obj]
        elif isinstance(obj, float):
            return Decimal(str(obj))
        return obj
