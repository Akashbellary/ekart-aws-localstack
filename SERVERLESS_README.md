# 🚀 EKart Store - Serverless Architecture Guide

## Overview

**EKart Store** is now a **fully serverless e-commerce application** running on AWS services through LocalStack. The entire backend runs on Lambda functions with API Gateway, eliminating the need to run a local backend server.

## Architecture

### Serverless Stack
- **Frontend**: Next.js (React)
- **API Gateway**: Routes HTTP requests to Lambda functions
- **Lambda Functions**: Serverless backend logic
- **DynamoDB**: NoSQL database for all data storage
- **Cognito**: User authentication and authorization
- **S3**: Product image storage
- **LocalStack**: Local AWS cloud stack for development

### Key Features
✅ **No local backend server required**
✅ **AWS Cognito authentication**
✅ **Fully serverless API**
✅ **Auto-scaling Lambda functions**
✅ **RESTful API Gateway**
✅ **Real AWS architecture in local development**

---

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- Docker & Docker Compose
- AWS CLI (optional, for testing)

### Installation

1. **Start LocalStack**:
```powershell
docker-compose up localstack
```

2. **Deploy Serverless Infrastructure** (one command):
```powershell
python scripts\deploy-serverless.py
```

3. **Seed Database**:
```powershell
python scripts\seed-products-corrected.py
```

4. **Configure Frontend**:
```powershell
python scripts\configure-frontend.py
```

5. **Start Frontend**:
```powershell
cd frontend
npm install  # First time only
npm run dev
```

6. **Access Application**:
   - Frontend: http://localhost:3000
   - API Gateway: See `serverless-config.json` for URL

---

## Lambda Functions

### 1. Auth API (`ekart-auth-api`)
**Routes**: `/api/auth/*`

- `POST /api/auth/register` - Register new user with Cognito
- `POST /api/auth/login` - Login with email/password
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user info

**Authentication**: Uses AWS Cognito User Pools

### 2. Products API (`ekart-products-api`)
**Routes**: `/api/products/*`

- `GET /api/products` - List all products (with filters)
- `GET /api/products/{id}` - Get single product
- `POST /api/products` - Create product (seller only, requires auth)
- `PUT /api/products/{id}` - Update product (seller only, requires auth)
- `DELETE /api/products/{id}` - Delete product (seller only, requires auth)

**Query Parameters**:
- `category` - Filter by category
- `seller_id` - Filter by seller
- `search` - Search in name/description

### 3. Cart API (`ekart-cart-api`)
**Routes**: `/api/cart/*`
**Authentication**: Required

- `GET /api/cart` - Get user's cart
- `POST /api/cart/items` - Add item to cart
- `PUT /api/cart/items/{id}` - Update item quantity
- `DELETE /api/cart/items/{id}` - Remove item from cart
- `DELETE /api/cart` - Clear entire cart

### 4. Orders API (`ekart-orders-api`)
**Routes**: `/api/orders/*`
**Authentication**: Required

- `GET /api/orders` - Get user's orders (buyer or seller view)
- `GET /api/orders/{id}` - Get single order
- `POST /api/orders` - Create order from cart
- `PUT /api/orders/{id}/status` - Update order status (seller only)

---

## API Gateway Configuration

### Base URL
```
http://localhost:4566/restapis/{api-id}/dev/_user_request_
```

The API ID is displayed after deployment and saved in `serverless-config.json`.

### CORS
All endpoints support CORS with:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET,POST,PUT,DELETE,OPTIONS`
- `Access-Control-Allow-Headers: Content-Type,Authorization`

### Authentication
Protected endpoints require `Authorization` header:
```
Authorization: Bearer {access_token}
```

Get access token from login/register response.

---

## AWS Cognito Integration

### User Registration
```bash
POST /api/auth/register
{
  "email": "user@example.com",
  "password": "Password123",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "customer"  # or "seller"
}
```

**Response**:
```json
{
  "access_token": "eyJraWQiOi...",
  "id_token": "eyJraWQiOi...",
  "refresh_token": "eyJjdHkiOi...",
  "user_id": "uuid",
  "email": "user@example.com",
  "user_type": "customer"
}
```

### User Login
```bash
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "Password123"
}
```

Returns same response as registration.

### Using Tokens
Include access token in subsequent requests:
```bash
GET /api/cart
Authorization: Bearer {access_token}
```

---

## DynamoDB Tables

1. **ekart-users-dev**
   - Primary Key: `user_id`
   - GSI: `email-index` on `email`

2. **ekart-products-dev**
   - Primary Key: `product_id`
   - GSI: `seller-index` on `seller_id`
   - GSI: `category-index` on `category`

3. **ekart-orders-dev**
   - Primary Key: `order_id`
   - GSI: `buyer-index` on `buyer_id`
   - GSI: `seller-index` on `seller_id`

4. **ekart-carts-dev**
   - Primary Key: `user_id`

5. **ekart-inventory-dev**
   - Primary Key: `product_id`

---

## Deployment Process

The `deploy-serverless.py` script performs the following:

1. **Create AWS Clients** - Initialize boto3 clients for LocalStack
2. **Create DynamoDB Tables** - All 5 tables with indexes
3. **Create Cognito User Pool** - With custom attributes for user_type
4. **Create S3 Buckets** - For images and Lambda code
5. **Create IAM Role** - For Lambda execution
6. **Package Lambda Functions** - ZIP each function directory
7. **Deploy Lambda Functions** - Create/update all 4 Lambda functions
8. **Create API Gateway** - REST API with all routes
9. **Configure Integrations** - Connect API Gateway to Lambda
10. **Deploy API Stage** - Deploy to 'dev' stage
11. **Save Configuration** - Write `serverless-config.json`

---

## Project Structure

```
ekart-store/
├── lambda-functions/          # Serverless backend
│   ├── auth-api/              # Authentication Lambda
│   │   ├── handler.py
│   │   └── requirements.txt
│   ├── products-api/          # Products Lambda
│   │   ├── handler.py
│   │   └── requirements.txt
│   ├── cart-api/              # Cart Lambda
│   │   ├── handler.py
│   │   └── requirements.txt
│   └── orders-api/            # Orders Lambda
│       ├── handler.py
│       └── requirements.txt
├── frontend/                  # Next.js frontend
│   ├── src/
│   └── .env.local            # Auto-generated config
├── scripts/
│   ├── deploy-serverless.py  # Main deployment script
│   ├── configure-frontend.py # Frontend config generator
│   └── seed-products-corrected.py
├── backend/                   # OLD - No longer needed
├── serverless-config.json     # Auto-generated
└── COMMANDS_SERVERLESS.md     # This guide
```

---

## Testing

### Manual API Testing

```powershell
# Set environment
$env:AWS_ACCESS_KEY_ID="test"
$env:AWS_SECRET_ACCESS_KEY="test"
$env:AWS_DEFAULT_REGION="us-east-1"

# Get API URL from config
$config = Get-Content serverless-config.json | ConvertFrom-Json
$API_URL = $config.api_url

# Test products endpoint
curl "$API_URL/api/products"

# Register user
curl -X POST "$API_URL/api/auth/register" `
  -H "Content-Type: application/json" `
  -d '{"email":"test@test.com","password":"Test123","first_name":"Test","last_name":"User","user_type":"customer"}'
```

### Lambda Testing

```powershell
# Invoke Lambda directly
aws lambda invoke `
  --function-name ekart-products-api `
  --endpoint-url=http://localhost:4566 `
  --payload '{"httpMethod":"GET","path":"/api/products"}' `
  response.json

cat response.json
```

---

## Troubleshooting

### Check LocalStack Services
```powershell
curl http://localhost:4566/_localstack/health
```

### View Lambda Logs
```powershell
docker-compose logs localstack | Select-String "Lambda"
```

### Redeploy Everything
```powershell
docker-compose down -v
docker-compose up localstack
# Wait 20 seconds
python scripts\deploy-serverless.py
python scripts\seed-products-corrected.py
python scripts\configure-frontend.py
```

### Check Deployment Config
```powershell
cat serverless-config.json
```

### Verify DynamoDB Tables
```powershell
aws dynamodb list-tables --endpoint-url=http://localhost:4566
```

### Verify Lambda Functions
```powershell
aws lambda list-functions --endpoint-url=http://localhost:4566
```

### Verify API Gateway
```powershell
aws apigateway get-rest-apis --endpoint-url=http://localhost:4566
```

---

## Migrating from Old Backend

If you were using the old FastAPI backend (`uvicorn`), here's what changed:

### Before:
```
Frontend → http://localhost:8000/api → FastAPI → AWS
```

### After:
```
Frontend → http://localhost:4566/restapis/{id}/dev/_user_request_/api → API Gateway → Lambda → AWS
```

### Changes Required:
1. **No backend server** - Don't run `uvicorn` anymore
2. **Update frontend env** - Use `configure-frontend.py`
3. **Use Cognito auth** - Not hash-based tokens
4. **API Gateway URL** - Different URL format

---

## Production Deployment

To deploy to real AWS (not LocalStack):

1. Remove `endpoint_url` from boto3 clients in `deploy-serverless.py`
2. Configure AWS credentials: `aws configure`
3. Update `ENDPOINT` variable to use real AWS endpoints
4. Run deployment script
5. Update frontend with real Cognito and API Gateway URLs

---

## Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:4566/restapis/{id}/dev/_user_request_
NEXT_PUBLIC_AWS_REGION=us-east-1
NEXT_PUBLIC_USER_POOL_ID={pool-id}
NEXT_PUBLIC_CLIENT_ID={client-id}
NEXT_PUBLIC_AWS_ENDPOINT=http://localhost:4566
```

Auto-generated by `configure-frontend.py`.

### Lambda Functions
Set via deployment script:
- `USER_POOL_ID`
- `CLIENT_ID`
- `PRODUCTS_TABLE`, `ORDERS_TABLE`, etc.
- `AWS_ENDPOINT_URL`

---

## Benefits of Serverless Architecture

✅ **No server management** - AWS handles scaling
✅ **Pay per use** - Only pay for actual requests
✅ **Auto-scaling** - Handles traffic spikes automatically
✅ **Microservices** - Each API is independent
✅ **Real AWS patterns** - Production-ready architecture
✅ **Easy deployment** - Single command deployment
✅ **Better security** - Cognito handles authentication

---

## Support

For issues or questions:
1. Check `COMMANDS_SERVERLESS.md` for detailed commands
2. Verify LocalStack is running: `curl http://localhost:4566/_localstack/health`
3. Check deployment config: `cat serverless-config.json`
4. View logs: `docker-compose logs localstack`

---

**Happy coding! 🚀**
