from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict
from decimal import Decimal

from services.mock_payment_service import payment_service
from services.cart_service import CartService
from services.product_service import ProductService
from services.auth_service import get_current_user
from models.user import UserProfile

router = APIRouter(prefix="/api/payments", tags=["payments"])

# Initialize service instances
# Using mock payment service since LocalStack Stripe extension returns empty responses
cart_service = CartService()
product_service = ProductService()

class CreatePaymentIntentRequest(BaseModel):
    amount: Optional[Decimal] = None  # If not provided, will calculate from cart
    currency: str = "usd"
    metadata: Optional[Dict] = None

class ConfirmPaymentRequest(BaseModel):
    payment_intent_id: str

@router.post("/create-payment-intent")
async def create_payment_intent(
    request: CreatePaymentIntentRequest,
    current_user: UserProfile = Depends(get_current_user)
):
    """
    Create a Stripe Payment Intent
    If amount is not provided, calculates from user's cart
    """
    try:
        amount = request.amount
        
        # If no amount provided, calculate from cart
        if amount is None:
            cart = await cart_service.get_cart(current_user.user_id)
            
            if not cart or not cart.get('items'):
                raise HTTPException(status_code=400, detail="Cart is empty")
            
            # Calculate total from cart items
            total = Decimal('0')
            for item in cart['items']:
                # Fetch product to get price
                product = await product_service.get_product_by_id(item['product_id'])
                if product:
                    price = Decimal(str(product.price))
                    quantity = Decimal(str(item.get('quantity', 1)))
                    total += price * quantity
            
            amount = total
        
        if amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be greater than 0")
        
        # Create payment intent with user metadata
        metadata = request.metadata or {}
        metadata['user_id'] = current_user.user_id
        metadata['user_email'] = current_user.email
        
        result = await payment_service.create_payment_intent(
            amount=amount,
            currency=request.currency,
            metadata=metadata
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"Error creating payment intent: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/confirm-payment")
async def confirm_payment(
    request: ConfirmPaymentRequest,
    current_user: UserProfile = Depends(get_current_user)
):
    """
    Confirm a payment intent
    """
    try:
        result = await payment_service.confirm_payment(request.payment_intent_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/payment-intent/{payment_intent_id}")
async def get_payment_intent(
    payment_intent_id: str,
    current_user: UserProfile = Depends(get_current_user)
):
    """
    Retrieve payment intent details
    """
    try:
        result = await payment_service.retrieve_payment_intent(payment_intent_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/config")
async def get_stripe_config():
    """
    Get Stripe publishable key for frontend
    """
    import os
    return {
        "publishable_key": os.getenv('STRIPE_PUBLISHABLE_KEY', 'pk_test_123'),
        "api_base": os.getenv('STRIPE_API_BASE', 'http://localhost:4566')
    }
