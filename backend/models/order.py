from pydantic import BaseModel, validator
from typing import Optional, List, Dict
from datetime import datetime
from decimal import Decimal
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class PaymentMethod(str, Enum):
    CARD = "card"
    PAYPAL = "paypal"
    WALLET = "wallet"
    COD = "cod"

class OrderItem(BaseModel):
    product_id: str
    variant_id: Optional[str] = None
    quantity: int
    unit_price: Decimal
    total_price: Decimal
    product_title: str
    seller_id: str
    
    @validator('quantity')
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v

class ShippingAddress(BaseModel):
    full_name: str
    address_line_1: str
    address_line_2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str
    phone: Optional[str] = None

class OrderCreate(BaseModel):
    items: List[OrderItem]
    shipping_address: ShippingAddress
    payment_method: PaymentMethod
    notes: Optional[str] = None

class Order(BaseModel):
    order_id: str
    buyer_id: str
    items: List[OrderItem]
    subtotal: Decimal
    tax_amount: Decimal
    shipping_cost: Decimal
    total_amount: Decimal
    currency: str = "USD"
    
    status: OrderStatus = OrderStatus.PENDING
    payment_status: PaymentStatus = PaymentStatus.PENDING
    payment_method: PaymentMethod
    
    shipping_address: ShippingAddress
    tracking_number: Optional[str] = None
    notes: Optional[str] = None
    
    created_at: datetime
    updated_at: datetime
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    tracking_number: Optional[str] = None
    notes: Optional[str] = None
