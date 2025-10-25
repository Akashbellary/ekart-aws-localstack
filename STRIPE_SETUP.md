# Stripe Payment Integration with LocalStack

This guide explains how to set up and use the Stripe payment integration with LocalStack's Stripe extension.

## Setup Steps

### 1. Install Backend Dependencies

```powershell
cd backend
pip install stripe==8.0.0
```

### 2. Install Frontend Dependencies

```powershell
cd frontend
npm install @stripe/stripe-js@^2.4.0 @stripe/react-stripe-js@^2.4.0
```

### 3. Verify LocalStack Stripe Extension

The Stripe extension should already be installed as shown in your output:
```
localstack-extension-stripe │ LocalStack Extension: Stripe │ 0.1.0
```

### 4. Restart Backend Server

```powershell
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Restart Frontend

```powershell
cd frontend
npm run dev
```

## How It Works

### Backend Architecture

1. **Payment Service** (`backend/services/payment_service.py`)
   - Configured to use LocalStack endpoint: `http://localhost:4566`
   - Creates Stripe Payment Intents
   - Handles payment confirmation and retrieval

2. **Payment API Routes** (`backend/api/payments/routes.py`)
   - `POST /api/payments/create-payment-intent` - Creates payment intent from cart
   - `POST /api/payments/confirm-payment` - Confirms payment
   - `GET /api/payments/payment-intent/{id}` - Retrieves payment details
   - `GET /api/payments/config` - Returns Stripe public key for frontend

3. **Environment Configuration** (`.env`)
   - `STRIPE_API_KEY=sk_test_123` - Test secret key
   - `STRIPE_PUBLISHABLE_KEY=pk_test_123` - Test publishable key
   - `STRIPE_API_BASE=http://localhost:4566` - Points to LocalStack

### Frontend Architecture

1. **Checkout Page** (`frontend/src/app/checkout/page.tsx`)
   - Fetches cart items and calculates total
   - Creates payment intent via backend API
   - Loads Stripe.js configured for LocalStack
   - Displays Stripe Payment Element for card input
   - Handles payment submission

2. **Success Page** (`frontend/src/app/checkout/success/page.tsx`)
   - Displays success message after payment
   - Shows payment intent ID
   - Provides navigation to orders/products

3. **Cart Integration**
   - "Proceed to Checkout" button routes to `/checkout`
   - Cart data is automatically passed to checkout

## Usage Flow

1. **User adds items to cart** → Navigate to `/cart`
2. **Click "Proceed to Checkout"** → Routes to `/checkout`
3. **Checkout page**:
   - Fetches Stripe configuration from backend
   - Retrieves cart items
   - Calculates total amount
   - Creates payment intent
   - Displays Stripe payment form
4. **User enters card details** → Test card: `4242 4242 4242 4242`
5. **Click "Pay Now"** → Payment processed via LocalStack Stripe
6. **Redirect to success page** → `/checkout/success`

## Testing with LocalStack Stripe

### Test Card Numbers

LocalStack Stripe extension supports standard test cards:

- **Success**: `4242 4242 4242 4242`
- **Decline**: `4000 0000 0000 0002`
- **Insufficient funds**: `4000 0000 0000 9995`
- **Expired card**: Use any past expiry date
- **CVC**: Any 3 digits
- **Zip**: Any 5 digits

### Verify Payments

You can check payment intents in LocalStack:

```powershell
# List payment intents
curl http://localhost:4566/_localstack/stripe/payment_intents

# Get specific payment intent
curl http://localhost:4566/_localstack/stripe/payment_intents/{payment_intent_id}
```

## API Endpoints

### Create Payment Intent
```
POST http://localhost:8000/api/payments/create-payment-intent
Authorization: Bearer {access_token}

Request Body:
{
  "currency": "usd",
  "metadata": {
    "user_id": "123",
    "cart_items": "[...]"
  }
}

Response:
{
  "client_secret": "pi_xxx_secret_xxx",
  "payment_intent_id": "pi_xxx",
  "amount": 5999,
  "currency": "usd",
  "status": "requires_payment_method"
}
```

### Get Stripe Config
```
GET http://localhost:8000/api/payments/config

Response:
{
  "publishable_key": "pk_test_123",
  "api_base": "http://localhost:4566"
}
```

## Troubleshooting

### Issue: "Stripe not found"
**Solution**: Make sure LocalStack is running and Stripe extension is installed
```powershell
localstack status
localstack extensions list
```

### Issue: "Payment failed"
**Solution**: Check LocalStack logs
```powershell
localstack logs
```

### Issue: "Cart is empty"
**Solution**: Add items to cart before proceeding to checkout

### Issue: "401 Unauthorized"
**Solution**: Make sure you're logged in and have valid access token

## Architecture Notes

### Why LocalStack Stripe Extension?

1. **Local Development**: Test payments without hitting real Stripe API
2. **No Network Dependency**: Works offline
3. **Free Testing**: No test mode charges
4. **Consistent Behavior**: Mimics Stripe production behavior
5. **Fast Iteration**: No rate limits or delays

### Payment Flow

```
User Cart → Checkout Page
              ↓
        Create Payment Intent
              ↓
        Backend API → LocalStack Stripe
              ↓
        Return Client Secret
              ↓
        Stripe.js Elements
              ↓
        User Enters Card
              ↓
        Confirm Payment → LocalStack Stripe
              ↓
        Success Page
```

### Security Considerations

- All API calls require authentication
- Payment intents include user metadata
- Client secret is single-use
- Stripe handles card details (PCI compliant)
- Never store card numbers

## Next Steps

1. **Order Creation**: After successful payment, create order in DynamoDB
2. **Inventory Management**: Deduct stock quantities
3. **Email Notifications**: Send order confirmation
4. **Webhook Handling**: Process Stripe webhooks for payment events
5. **Refunds**: Implement refund functionality
6. **Subscription Support**: Add recurring payments if needed

## References

- [LocalStack Stripe Extension](https://blog.localstack.cloud/2022-09-12-announcing-localstack-extensions/)
- [Stripe API Documentation](https://stripe.com/docs/api)
- [Stripe.js Reference](https://stripe.com/docs/js)
- [Payment Element](https://stripe.com/docs/payments/payment-element)
