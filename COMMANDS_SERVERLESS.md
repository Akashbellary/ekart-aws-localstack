# 🚀 Complete Command Reference - Serverless Architecture

## ⚡ **NEW: Serverless Deployment (No Backend Server Required!)**

This project now runs **entirely on AWS services** (LocalStack). You don't need to run the backend server locally anymore!

---

## Quick Start (3 Steps)

### **Terminal 1 - Start LocalStack**
```powershell
docker-compose up localstack
```
*Wait 15-20 seconds for LocalStack to be ready*

---

### **Terminal 2 - Deploy Everything (One Command)**
```powershell
# Deploy all AWS infrastructure, Lambda functions, and API Gateway
python scripts\deploy-serverless.py

# Seed the database with products
python scripts\seed-products-corrected.py

# Configure frontend with API endpoints
python scripts\configure-frontend.py
```

---

### **Terminal 3 - Start Frontend**
```powershell
cd frontend
npm run dev
```

**That's it!** 🎉 Your entire backend is now running on AWS Lambda + API Gateway!

- Frontend: http://localhost:3000
- API Gateway: (URL will be displayed after deployment)

---

## What Gets Deployed?

The `deploy-serverless.py` script deploys:

1. **DynamoDB Tables**: Users, Products, Orders, Carts, Inventory
2. **AWS Cognito**: User authentication with user pools
3. **S3 Buckets**: Product images storage
4. **Lambda Functions**:
   - `ekart-auth-api` - Authentication (register, login)
   - `ekart-products-api` - Product CRUD operations
   - `ekart-cart-api` - Shopping cart management
   - `ekart-orders-api` - Order processing
5. **API Gateway**: RESTful API with routes:
   - `/api/auth/*` → Auth Lambda
   - `/api/products/*` → Products Lambda
   - `/api/cart/*` → Cart Lambda
   - `/api/orders/*` → Orders Lambda

---

## Architecture Changes

### Before (Required Local Backend):
```
Frontend (Next.js) → Backend (FastAPI/uvicorn) → AWS Services
     :3000                    :8000
```

### After (Fully Serverless):
```
Frontend (Next.js) → API Gateway → Lambda Functions → DynamoDB/Cognito/S3
     :3000              :4566
```

✅ **No need to run `uvicorn` or any backend server!**
✅ **Everything runs on AWS services through LocalStack**

---

## Detailed Deployment Steps

### Step 1: Start LocalStack
```powershell
# Start only LocalStack
docker-compose up localstack

# Or start all services (but backend is no longer needed)
docker-compose up
```

### Step 2: Deploy Serverless Infrastructure
```powershell
python scripts\deploy-serverless.py
```

This will output:
```
📋 DEPLOYMENT SUMMARY:
  • API Gateway URL: http://localhost:4566/restapis/{api-id}/dev/_user_request_
  • Cognito User Pool ID: us-east-1_xxxxxxx
  • Cognito Client ID: xxxxxxxxxxxxx
```

### Step 3: Seed Database
```powershell
# Seed with 39 sample products
python scripts\seed-products-corrected.py

# Optional: Add more products
python scripts\seed-data.py
```

### Step 4: Configure Frontend
```powershell
# Auto-configure frontend with API Gateway URL
python scripts\configure-frontend.py
```

This creates `frontend/.env.local` with:
- API Gateway URL
- Cognito User Pool ID
- Cognito Client ID

### Step 5: Start Frontend
```powershell
cd frontend
npm run dev
```

---

## Authentication with AWS Cognito

The project now uses **AWS Cognito** for authentication instead of simple hash-based auth:

### Register a User (via Frontend or API):
```powershell
# Via API (using curl)
curl -X POST http://localhost:4566/restapis/{API_ID}/dev/_user_request_/api/auth/register `
  -H "Content-Type: application/json" `
  -d '{
    "email": "seller@example.com",
    "password": "Test1234",
    "first_name": "John",
    "last_name": "Seller",
    "user_type": "seller"
  }'
```

### Login:
```powershell
curl -X POST http://localhost:4566/restapis/{API_ID}/dev/_user_request_/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{
    "email": "seller@example.com",
    "password": "Test1234"
  }'
```

Returns:
```json
{
  "access_token": "eyJraWQ...",
  "id_token": "eyJraWQ...",
  "refresh_token": "eyJjdH...",
  "user_id": "xxxxx-xxxxx",
  "email": "seller@example.com",
  "user_type": "seller"
}
```

Use the `access_token` in Authorization header:
```powershell
Authorization: Bearer eyJraWQ...
```

---

## Testing the API

### Get All Products:
```powershell
curl http://localhost:4566/restapis/{API_ID}/dev/_user_request_/api/products
```

### Get Single Product:
```powershell
curl http://localhost:4566/restapis/{API_ID}/dev/_user_request_/api/products/{product_id}
```

### Add to Cart (Requires Auth):
```powershell
curl -X POST http://localhost:4566/restapis/{API_ID}/dev/_user_request_/api/cart/items `
  -H "Authorization: Bearer {ACCESS_TOKEN}" `
  -H "Content-Type: application/json" `
  -d '{
    "product_id": "{PRODUCT_ID}",
    "quantity": 2
  }'
```

### Get Cart:
```powershell
curl http://localhost:4566/restapis/{API_ID}/dev/_user_request_/api/cart `
  -H "Authorization: Bearer {ACCESS_TOKEN}"
```

### Create Order:
```powershell
curl -X POST http://localhost:4566/restapis/{API_ID}/dev/_user_request_/api/orders `
  -H "Authorization: Bearer {ACCESS_TOKEN}" `
  -H "Content-Type: application/json" `
  -d '{
    "shipping_address": {
      "street": "123 Main St",
      "city": "New York",
      "state": "NY",
      "zip": "10001"
    },
    "payment_method": "card"
  }'
```

---

## Checking Lambda Functions

### List all Lambda functions:
```powershell
aws lambda list-functions --endpoint-url=http://localhost:4566
```

### Invoke Lambda directly:
```powershell
aws lambda invoke `
  --function-name ekart-products-api `
  --endpoint-url=http://localhost:4566 `
  --payload '{"httpMethod":"GET","path":"/api/products"}' `
  response.json

cat response.json
```

### View Lambda logs:
```powershell
docker-compose logs localstack | Select-String "ekart-"
```

---

## Checking API Gateway

### List APIs:
```powershell
aws apigateway get-rest-apis --endpoint-url=http://localhost:4566
```

### Get API Resources:
```powershell
aws apigateway get-resources `
  --rest-api-id {API_ID} `
  --endpoint-url=http://localhost:4566
```

---

## Troubleshooting

### Check LocalStack Health:
```powershell
curl http://localhost:4566/_localstack/health
```

Should show:
```json
{
  "services": {
    "apigateway": "running",
    "cognito-idp": "running",
    "dynamodb": "running",
    "lambda": "running",
    "s3": "running"
  }
}
```

### Redeploy Everything:
```powershell
# Stop LocalStack
docker-compose down

# Remove volumes (fresh start)
docker-compose down -v

# Start LocalStack
docker-compose up localstack

# Wait 15-20 seconds, then redeploy
python scripts\deploy-serverless.py
python scripts\seed-products-corrected.py
python scripts\configure-frontend.py
```

### View Deployment Config:
```powershell
cat serverless-config.json
```

Contains all API URLs and IDs for reference.

---

## AWS CLI Commands (LocalStack)

### Set Environment Variables:
```powershell
$env:AWS_ACCESS_KEY_ID="test"
$env:AWS_SECRET_ACCESS_KEY="test"
$env:AWS_DEFAULT_REGION="us-east-1"
```

### DynamoDB:
```powershell
# List tables
aws dynamodb list-tables --endpoint-url=http://localhost:4566

# Scan products
aws dynamodb scan --table-name ekart-products-dev --endpoint-url=http://localhost:4566
```

### Cognito:
```powershell
# List user pools
aws cognito-idp list-user-pools --max-results 10 --endpoint-url=http://localhost:4566

# List users
aws cognito-idp list-users --user-pool-id {USER_POOL_ID} --endpoint-url=http://localhost:4566
```

---

## Development Workflow

### Making Changes to Lambda Functions:

1. Edit code in `lambda-functions/{function-name}/handler.py`
2. Redeploy:
   ```powershell
   python scripts\deploy-serverless.py
   ```
3. Test the API endpoint

### Making Changes to Frontend:

1. Edit code in `frontend/src/`
2. Hot reload automatically refreshes browser
3. No redeployment needed

---

## Clean Up

### Stop Everything:
```powershell
# Stop frontend
Ctrl+C in frontend terminal

# Stop LocalStack
docker-compose down
```

### Remove All Data:
```powershell
docker-compose down -v
```

---

## Old Backend (No Longer Needed)

The `backend/` directory with FastAPI code is **no longer required** for running the application. All backend logic is now in Lambda functions.

If you want to use the old architecture:
```powershell
# Terminal 1: LocalStack
docker-compose up localstack

# Terminal 2: Old deployment
python scripts\deploy-infrastructure.py
python scripts\seed-products-corrected.py

# Terminal 3: Backend (old way)
cd backend
uvicorn main:app --reload

# Terminal 4: Frontend
cd frontend
npm run dev
```

But the **recommended way** is the new serverless architecture! 🚀

---

## Summary of Commands

### Complete Serverless Deployment:
```powershell
# Terminal 1
docker-compose up localstack

# Terminal 2 (after LocalStack is ready)
python scripts\deploy-serverless.py
python scripts\seed-products-corrected.py
python scripts\configure-frontend.py

# Terminal 3
cd frontend
npm run dev
```

### Access Points:
- **Frontend**: http://localhost:3000
- **API Gateway**: Check `serverless-config.json` for URL
- **LocalStack**: http://localhost:4566
- **LocalStack Health**: http://localhost:4566/_localstack/health

---

**🎉 Enjoy your fully serverless e-commerce application!**

All backend logic runs on AWS Lambda + API Gateway through LocalStack. No need to manage backend servers anymore!
