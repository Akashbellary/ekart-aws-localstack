from typing import List, Optional
from models.product import Product, ProductCreate, ProductUpdate, ProductFilter, ProductSearchQuery
from config.database import dynamodb, PRODUCTS_TABLE, INVENTORY_TABLE
from datetime import datetime
from decimal import Decimal
import uuid

class ProductService:
    def __init__(self):
        self.products_table = dynamodb.Table(PRODUCTS_TABLE)
        self.inventory_table = dynamodb.Table(INVENTORY_TABLE)

    async def get_products(self, filters: ProductFilter, page: int = 1, per_page: int = 20) -> List[Product]:
        """Get products with filters and pagination"""
        try:
            response = self.products_table.scan(Limit=per_page)
            items = response.get('Items', [])
            return [Product(**self._convert_decimals(item)) for item in items]
        except Exception as e:
            print(f"Error getting products: {e}")
            return []

    async def search_products(self, search_query: ProductSearchQuery) -> List[Product]:
        """Search products by query"""
        # For now, return all products (implement search logic later)
        return await self.get_products(search_query.filters or ProductFilter(), search_query.page, search_query.per_page)

    async def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """Get a specific product by ID"""
        try:
            response = self.products_table.get_item(Key={'product_id': product_id})
            if 'Item' in response:
                return Product(**self._convert_decimals(response['Item']))
            return None
        except Exception as e:
            print(f"Error getting product: {e}")
            return None

    async def create_product(self, product_id: str, seller_id: str, product_data: ProductCreate) -> Product:
        """Create a new product"""
        now = datetime.utcnow().isoformat()
        product = {
            'product_id': product_id,
            'seller_id': seller_id,
            'title': product_data.title,
            'description': product_data.description,
            'category': product_data.category,
            'price': Decimal(str(product_data.price)),
            'currency': product_data.currency,
            'stock_quantity': product_data.stock_quantity,
            'is_active': True,
            'rating': None,
            'review_count': 0,
            'images': [],
            'variants': [],
            'tags': product_data.tags or [],
            'brand': product_data.brand,
            'created_at': now,
            'updated_at': now
        }
        
        self.products_table.put_item(Item=product)
        
        # Create inventory entry
        self.inventory_table.put_item(Item={
            'product_id': product_id,
            'stock_quantity': product_data.stock_quantity
        })
        
        return Product(**product)

    async def update_product(self, product_id: str, product_data: ProductUpdate) -> Optional[Product]:
        """Update a product"""
        update_expr = "SET updated_at = :updated_at"
        expr_values = {':updated_at': datetime.utcnow().isoformat()}
        
        if product_data.title:
            update_expr += ", title = :title"
            expr_values[':title'] = product_data.title
        if product_data.description:
            update_expr += ", description = :description"
            expr_values[':description'] = product_data.description
        if product_data.price:
            update_expr += ", price = :price"
            expr_values[':price'] = Decimal(str(product_data.price))
        if product_data.stock_quantity is not None:
            update_expr += ", stock_quantity = :stock"
            expr_values[':stock'] = product_data.stock_quantity
        if product_data.is_active is not None:
            update_expr += ", is_active = :active"
            expr_values[':active'] = product_data.is_active
        
        self.products_table.update_item(
            Key={'product_id': product_id},
            UpdateExpression=update_expr,
            ExpressionAttributeValues=expr_values
        )
        
        return await self.get_product_by_id(product_id)

    async def delete_product(self, product_id: str):
        """Delete a product"""
        self.products_table.delete_item(Key={'product_id': product_id})
        self.inventory_table.delete_item(Key={'product_id': product_id})

    async def add_product_images(self, product_id: str, image_urls: List[str]):
        """Add images to a product"""
        images = [{'image_id': str(uuid.uuid4()), 'url': url, 'is_primary': i == 0} 
                  for i, url in enumerate(image_urls)]
        
        self.products_table.update_item(
            Key={'product_id': product_id},
            UpdateExpression="SET images = :images",
            ExpressionAttributeValues={':images': images}
        )

    async def get_categories(self):
        """Get all product categories"""
        return [
            {'id': 'electronics', 'name': 'Electronics', 'icon': '💻', 'slug': 'electronics'},
            {'id': 'fashion', 'name': 'Fashion', 'icon': '👔', 'slug': 'fashion'},
            {'id': 'home', 'name': 'Home & Garden', 'icon': '🏠', 'slug': 'home'},
            {'id': 'sports', 'name': 'Sports', 'icon': '⚽', 'slug': 'sports'},
            {'id': 'books', 'name': 'Books', 'icon': '📚', 'slug': 'books'},
            {'id': 'toys', 'name': 'Toys', 'icon': '🎮', 'slug': 'toys'}
        ]

    def _convert_decimals(self, obj):
        """Convert DynamoDB Decimals to floats"""
        if isinstance(obj, list):
            return [self._convert_decimals(i) for i in obj]
        elif isinstance(obj, dict):
            return {k: self._convert_decimals(v) for k, v in obj.items()}
        elif isinstance(obj, Decimal):
            return float(obj)
        return obj
