from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List, Literal
from datetime import datetime
from enum import Enum

class UserType(str, Enum):
    BUYER = "buyer"
    SELLER = "seller"
    ADMIN = "admin"

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    user_type: UserType = UserType.BUYER

class UserCreate(UserBase):
    password: str
    confirm_password: str
    
    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

class UserProfile(UserBase):
    user_id: str
    is_verified: bool = False
    seller_verified: bool = False
    created_at: datetime
    updated_at: datetime
    
    # Seller specific fields
    business_name: Optional[str] = None
    business_address: Optional[str] = None
    tax_id: Optional[str] = None
    bank_details: Optional[dict] = None

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    business_name: Optional[str] = None
    business_address: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    user_id: str
    email: str
    full_name: str
    user_type: UserType
    is_verified: bool
    seller_verified: bool
