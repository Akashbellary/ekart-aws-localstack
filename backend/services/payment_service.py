import stripe
import os
from typing import Dict, Optional
from decimal import Decimal

# Configure Stripe for LocalStack
stripe.api_key = os.getenv('STRIPE_API_KEY', 'sk_test_123')
stripe.api_base = os.getenv('STRIPE_API_BASE', 'http://localhost:4566')

class PaymentService:
    def __init__(self):
        self.currency = 'usd'
    
    async def create_payment_intent(
        self,
        amount: Decimal,
        currency: str = 'usd',
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Create a Stripe Payment Intent
        Amount should be in dollars, will be converted to cents
        """
        try:
            # Convert amount to cents (Stripe uses smallest currency unit)
            amount_cents = int(amount * 100)
            
            print(f"Creating payment intent for ${amount} ({amount_cents} cents)")
            
            # Create payment intent - simplified for LocalStack compatibility
            payment_intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency=currency,
                metadata=metadata or {},
                payment_method_types=['card'],
            )
            
            print(f"Payment intent created: {payment_intent.id}")
            
            return {
                'client_secret': payment_intent.client_secret,
                'payment_intent_id': payment_intent.id,
                'amount': amount_cents,
                'currency': currency,
                'status': payment_intent.status
            }
        except stripe.error.StripeError as e:
            print(f"Stripe error: {str(e)}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Stripe error: {str(e)}")
        except Exception as e:
            print(f"Payment service error: {str(e)}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Payment service error: {str(e)}")
    
    async def confirm_payment(self, payment_intent_id: str) -> Dict:
        """
        Confirm a payment intent
        """
        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            return {
                'payment_intent_id': payment_intent.id,
                'status': payment_intent.status,
                'amount': payment_intent.amount,
                'currency': payment_intent.currency
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")
        except Exception as e:
            raise Exception(f"Payment service error: {str(e)}")
    
    async def retrieve_payment_intent(self, payment_intent_id: str) -> Dict:
        """
        Retrieve payment intent details
        """
        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            return {
                'payment_intent_id': payment_intent.id,
                'status': payment_intent.status,
                'amount': payment_intent.amount / 100,  # Convert back to dollars
                'currency': payment_intent.currency,
                'metadata': payment_intent.metadata
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")
        except Exception as e:
            raise Exception(f"Payment service error: {str(e)}")
    
    async def create_checkout_session(
        self,
        line_items: list,
        success_url: str,
        cancel_url: str,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Create a Stripe Checkout Session
        """
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata=metadata or {}
            )
            
            return {
                'session_id': session.id,
                'url': session.url,
                'status': session.status
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")
        except Exception as e:
            raise Exception(f"Payment service error: {str(e)}")

payment_service = PaymentService()
