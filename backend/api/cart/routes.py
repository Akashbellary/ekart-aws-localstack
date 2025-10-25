from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.auth_service import get_current_user
from models.user import UserProfile
from services.cart_service import CartService

router = APIRouter()
cart_service = CartService()

class AddToCartRequest(BaseModel):
    product_id: str
    quantity: int = 1

@router.get("/")
async def get_cart(current_user: UserProfile = Depends(get_current_user)):
    """Get current user's cart"""
    cart = await cart_service.get_cart(current_user.user_id)
    return cart

@router.post("/items")
async def add_to_cart(request: AddToCartRequest, current_user: UserProfile = Depends(get_current_user)):
    """Add item to cart"""
    cart = await cart_service.add_item(current_user.user_id, request.product_id, request.quantity)
    return cart

@router.delete("/items/{product_id}")
async def remove_from_cart(product_id: str, current_user: UserProfile = Depends(get_current_user)):
    """Remove item from cart"""
    cart = await cart_service.remove_item(current_user.user_id, product_id)
    return cart

@router.put("/items/{product_id}")
async def update_cart_item(product_id: str, quantity: int, current_user: UserProfile = Depends(get_current_user)):
    """Update item quantity in cart"""
    cart = await cart_service.update_quantity(current_user.user_id, product_id, quantity)
    return cart
