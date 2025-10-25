from pydantic import BaseModel, validator
from typing import Optional, List, Dict
from datetime import datetime
from decimal import Decimal

class ProductCategory(BaseModel):
    category_id: str
    name: str
    description: Optional[str] = None

class ProductImage(BaseModel):
    image_id: Optional[str] = None
    url: str
    alt_text: Optional[str] = None
    is_primary: bool = False
    three_d_model_url: Optional[str] = None

class ProductVariant(BaseModel):
    variant_id: str
    name: str  # e.g., "Size", "Color"
    value: str  # e.g., "Large", "Red"
    price_modifier: Decimal = Decimal('0.00')
    stock_quantity: int = 0

class ProductBase(BaseModel):
    title: str
    description: str
    category: str
    price: Decimal
    currency: str = "USD"
    weight: Optional[float] = None
    dimensions: Optional[Dict[str, float]] = None  # {"length": 10, "width": 5, "height": 2}
    brand: Optional[str] = None
    tags: List[str] = []
    
    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v

class ProductCreate(ProductBase):
    stock_quantity: int = 0
    variants: List[ProductVariant] = []
    
    @validator('stock_quantity')
    def stock_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError('Stock quantity must be non-negative')
        return v

class Product(ProductBase):
    product_id: str
    seller_id: str
    stock_quantity: Optional[int] = 0
    stock: Optional[int] = 0  # Alternative field name
    variants: List[ProductVariant] = []
    images: List[ProductImage] = []
    is_active: bool = True
    rating: Optional[float] = None
    review_count: int = 0
    created_at: datetime
    updated_at: datetime
    
    @validator('stock_quantity', always=True)
    def set_stock_quantity(cls, v, values):
        # Use 'stock' field if stock_quantity is not provided
        if v is None or v == 0:
            return values.get('stock', 0)
        return v

class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    stock_quantity: Optional[int] = None
    is_active: Optional[bool] = None
    tags: Optional[List[str]] = None

class ProductFilter(BaseModel):
    category: Optional[str] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    brand: Optional[str] = None
    tags: Optional[List[str]] = None
    seller_id: Optional[str] = None
    in_stock: bool = True

class ProductSearchQuery(BaseModel):
    query: str
    filters: Optional[ProductFilter] = None
    sort_by: str = "relevance"  # relevance, price_asc, price_desc, rating, newest
    page: int = 1
    per_page: int = 20
