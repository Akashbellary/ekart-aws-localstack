from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
import hashlib
from datetime import datetime
from config.database import dynamodb, USERS_TABLE

router = APIRouter()

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    user_type: str = "customer"  # customer or seller

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    user_type: str

def hash_password(password: str) -> str:
    """Simple password hashing (in production, use bcrypt or similar)"""
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/register/", response_model=AuthResponse)
async def register(request: RegisterRequest):
    """Register a new user"""
    try:
        users_table = dynamodb.Table(USERS_TABLE)
        
        # Check if user already exists
        response = users_table.scan(
            FilterExpression='email = :email',
            ExpressionAttributeValues={':email': request.email}
        )
        
        if response.get('Items'):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        user_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        user_data = {
            'user_id': user_id,
            'email': request.email,
            'password_hash': hash_password(request.password),
            'first_name': request.first_name,
            'last_name': request.last_name,
            'phone': request.phone,
            'user_type': request.user_type,
            'is_active': True,
            'is_verified': False,
            'created_at': now,
            'updated_at': now
        }
        
        users_table.put_item(Item=user_data)
        
        # Generate simple token (in production, use JWT)
        access_token = f"{user_id}:{hash_password(f'{user_id}{request.email}')}"
        
        return AuthResponse(
            access_token=access_token,
            user_id=user_id,
            email=request.email,
            user_type=request.user_type
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.post("/login/", response_model=AuthResponse)
async def login(request: LoginRequest):
    """Login user"""
    try:
        users_table = dynamodb.Table(USERS_TABLE)
        
        # Find user by email
        response = users_table.scan(
            FilterExpression='email = :email',
            ExpressionAttributeValues={':email': request.email}
        )
        
        items = response.get('Items', [])
        if not items:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        user = items[0]
        
        # Verify password
        if user['password_hash'] != hash_password(request.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Generate token
        token_string = f"{user['user_id']}{request.email}"
        access_token = f"{user['user_id']}:{hash_password(token_string)}"
        
        return AuthResponse(
            access_token=access_token,
            user_id=user['user_id'],
            email=user['email'],
            user_type=user.get('user_type', 'customer')
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@router.post("/logout/")
async def logout():
    """Logout user (client-side token removal)"""
    return {"message": "Logged out successfully"}

@router.get("/me")
async def get_current_user_info():
    """Get current user info"""
    return {"message": "Get current user endpoint - to be implemented"}
