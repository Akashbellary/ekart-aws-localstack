from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.user import UserProfile
from typing import Optional
from config.database import dynamodb, USERS_TABLE

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UserProfile:
    """
    Get current authenticated user from token
    Token format: user_id:hash
    """
    try:
        token = credentials.credentials
        
        # Parse token (format: user_id:hash)
        parts = token.split(':')
        if len(parts) != 2:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format"
            )
        
        user_id = parts[0]
        
        # Get user from database
        users_table = dynamodb.Table(USERS_TABLE)
        response = users_table.get_item(Key={'user_id': user_id})
        
        if 'Item' not in response:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        user = response['Item']
        
        # Return UserProfile
        return UserProfile(
            user_id=user['user_id'],
            email=user['email'],
            full_name=f"{user.get('first_name', '')} {user.get('last_name', '')}".strip(),
            user_type=user.get('user_type', 'customer'),
            is_verified=user.get('is_verified', False),
            seller_verified=user.get('user_type') == 'seller',  # All sellers are verified for now
            created_at=user.get('created_at', ''),
            updated_at=user.get('updated_at', '')
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Auth error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

async def get_current_seller(
    current_user: UserProfile = Depends(get_current_user)
) -> UserProfile:
    """Get current user and verify they are a seller"""
    if current_user.user_type != "seller":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers can access this resource"
        )
    return current_user

async def get_current_admin(
    current_user: UserProfile = Depends(get_current_user)
) -> UserProfile:
    """Get current user and verify they are an admin"""
    if current_user.user_type != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access this resource"
        )
    return current_user
