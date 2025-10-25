import os
from typing import Dict, Optional
from decimal import Decimal
import uuid
from datetime import datetime

class MockPaymentService:
    """
    Mock payment service for local development when LocalStack Stripe is unavailable.
    Simulates Stripe API behavior without external dependencies.
    """
    
    def __init__(self):
        self.currency = 'usd'
        self.payments = {}  # In-memory storage for demo
    
    async def create_payment_intent(
        self,
        amount: Decimal,
        currency: str = 'usd',
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Create a mock payment intent
        """
        try:
            # Convert amount to cents
            amount_cents = int(amount * 100)
            
            # Generate mock payment intent with proper Stripe format
            # Format: pi_{random}_secret_{random}
            pi_id = uuid.uuid4().hex[:24]
            secret_id = uuid.uuid4().hex[:16]
            payment_intent_id = f"pi_{pi_id}"
            client_secret = f"pi_{pi_id}_secret_{secret_id}"
            
            payment_intent = {
                'id': payment_intent_id,
                'client_secret': client_secret,
                'amount': amount_cents,
                'currency': currency,
                'status': 'requires_payment_method',
                'metadata': metadata or {},
                'created': int(datetime.utcnow().timestamp())
            }
            
            # Store for later retrieval
            self.payments[payment_intent_id] = payment_intent
            
            print(f"Mock payment intent created: {payment_intent_id} for ${amount} ({amount_cents} cents)")
            
            return {
                'client_secret': client_secret,
                'payment_intent_id': payment_intent_id,
                'amount': amount_cents,
                'currency': currency,
                'status': 'requires_payment_method'
            }
        except Exception as e:
            print(f"Mock payment service error: {str(e)}")
            raise Exception(f"Payment service error: {str(e)}")
    
    async def confirm_payment(self, payment_intent_id: str) -> Dict:
        """
        Mock confirm payment
        """
        try:
            if payment_intent_id in self.payments:
                self.payments[payment_intent_id]['status'] = 'succeeded'
                payment_intent = self.payments[payment_intent_id]
            else:
                # Create a mock succeeded payment
                payment_intent = {
                    'id': payment_intent_id,
                    'status': 'succeeded',
                    'amount': 0,
                    'currency': 'usd'
                }
            
            return {
                'payment_intent_id': payment_intent['id'],
                'status': payment_intent['status'],
                'amount': payment_intent['amount'],
                'currency': payment_intent['currency']
            }
        except Exception as e:
            raise Exception(f"Payment service error: {str(e)}")
    
    async def retrieve_payment_intent(self, payment_intent_id: str) -> Dict:
        """
        Retrieve mock payment intent details
        """
        try:
            if payment_intent_id in self.payments:
                payment_intent = self.payments[payment_intent_id]
            else:
                # Return mock data
                payment_intent = {
                    'id': payment_intent_id,
                    'status': 'succeeded',
                    'amount': 0,
                    'currency': 'usd',
                    'metadata': {}
                }
            
            return {
                'payment_intent_id': payment_intent['id'],
                'status': payment_intent['status'],
                'amount': payment_intent['amount'] / 100,
                'currency': payment_intent['currency'],
                'metadata': payment_intent.get('metadata', {})
            }
        except Exception as e:
            raise Exception(f"Payment service error: {str(e)}")

# Use mock service for now since LocalStack Stripe extension isn't responding properly
payment_service = MockPaymentService()
