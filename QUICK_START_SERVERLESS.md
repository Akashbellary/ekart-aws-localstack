# 🚀 Quick Start - Serverless EKart Store

## Prerequisites Installed?
- ✅ Python 3.9+
- ✅ Node.js 16+
- ✅ Docker & Docker Compose

---

## 3-Step Deployment

### Step 1: Start LocalStack
Open **Terminal 1**:
```powershell
docker-compose up localstack
```

**Wait 15-20 seconds** for LocalStack to start.

---

### Step 2: Deploy Everything (One Command!)
Open **Terminal 2**:
```powershell
python scripts\quick-deploy.py
```

This script will:
- ✅ Deploy all AWS infrastructure (DynamoDB, Cognito, S3)
- ✅ Create Lambda functions
- ✅ Set up API Gateway
- ✅ Seed database with products
- ✅ Configure frontend automatically

**Takes about 30-60 seconds.**

---

### Step 3: Start Frontend
In **Terminal 2** (after deployment completes):
```powershell
cd frontend
npm install  # First time only
npm run dev
```

---

## Access Your Application

**Frontend**: http://localhost:3000

**API Gateway**: Check `serverless-config.json` for URL

---

## What Just Happened?

Your entire e-commerce application is now running on:
- 🔐 **AWS Cognito** - User authentication
- 🌐 **API Gateway** - RESTful API
- ⚡ **Lambda Functions** - Serverless backend (4 functions)
- 📦 **DynamoDB** - Database (5 tables)
- 🪣 **S3** - File storage

**All in LocalStack - No backend server needed!**

---

## Testing the Application

### 1. Register a User
1. Go to http://localhost:3000
2. Click "Register" or "Sign Up"
3. Fill in details:
   - Email: test@example.com
   - Password: Test1234
   - User Type: Customer or Seller
4. Submit

### 2. Browse Products
- View all products on homepage
- Click on product for details
- Add to cart

### 3. Checkout
- View cart
- Proceed to checkout
- Place order

### 4. Seller Features (if registered as seller)
- Add new products
- View your products
- Manage inventory

---

## Troubleshooting

### Problem: LocalStack not starting
```powershell
docker-compose down -v
docker-compose up localstack
```

### Problem: Deployment failed
```powershell
# Check LocalStack health
curl http://localhost:4566/_localstack/health

# If healthy, try again
python scripts\quick-deploy.py
```

### Problem: Frontend can't connect
```powershell
# Reconfigure frontend
python scripts\configure-frontend.py

# Verify .env.local exists
cat frontend\.env.local
```

### Fresh Start (Nuclear Option)
```powershell
# Terminal 1
docker-compose down -v
docker-compose up localstack

# Wait 20 seconds, then Terminal 2
python scripts\quick-deploy.py
cd frontend
npm run dev
```

---

## Manual Deployment (Alternative)

If `quick-deploy.py` doesn't work:

**Terminal 2:**
```powershell
python scripts\deploy-serverless.py
python scripts\seed-products-corrected.py
python scripts\configure-frontend.py
cd frontend
npm run dev
```

---

## Architecture

```
┌─────────────┐
│  Frontend   │  You access this
│  Next.js    │  http://localhost:3000
│   :3000     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│          LocalStack (:4566)             │
│  ┌─────────────┐    ┌────────────────┐ │
│  │ API Gateway │───►│ Lambda Funcs   │ │
│  └─────────────┘    │ • Auth API     │ │
│                     │ • Products API │ │
│  ┌─────────────┐    │ • Cart API     │ │
│  │  Cognito    │    │ • Orders API   │ │
│  │ (Auth)      │    └────────┬───────┘ │
│  └─────────────┘             │         │
│                              ▼         │
│  ┌─────────────┐    ┌────────────────┐ │
│  │  DynamoDB   │    │      S3        │ │
│  │  (5 tables) │    │   (Images)     │ │
│  └─────────────┘    └────────────────┘ │
└─────────────────────────────────────────┘
```

---

## What's Different from Before?

### ❌ OLD WAY:
```
Terminal 1: docker-compose up localstack
Terminal 2: python scripts/deploy-infrastructure.py
Terminal 3: uvicorn main:app --reload  ← Had to run backend
Terminal 4: npm run dev
```

### ✅ NEW WAY:
```
Terminal 1: docker-compose up localstack
Terminal 2: python scripts/quick-deploy.py
Terminal 2: cd frontend && npm run dev
```

**No backend server needed! Everything runs on Lambda.**

---

## API Endpoints

All via API Gateway:

**Public:**
- `GET /api/products` - List products
- `GET /api/products/{id}` - Get product
- `POST /api/auth/register` - Register
- `POST /api/auth/login` - Login

**Authenticated:**
- `POST /api/products` - Create product (seller)
- `GET /api/cart` - Get cart
- `POST /api/cart/items` - Add to cart
- `POST /api/orders` - Create order
- `GET /api/orders` - List orders

**Authentication:**
```
Authorization: Bearer {access_token}
```

---

## Useful Commands

**Check LocalStack:**
```powershell
curl http://localhost:4566/_localstack/health
```

**View Config:**
```powershell
cat serverless-config.json
```

**List Lambda Functions:**
```powershell
aws lambda list-functions --endpoint-url=http://localhost:4566
```

**List DynamoDB Tables:**
```powershell
aws dynamodb list-tables --endpoint-url=http://localhost:4566
```

**Scan Products:**
```powershell
aws dynamodb scan --table-name ekart-products-dev --endpoint-url=http://localhost:4566
```

---

## Need Help?

📚 **Documentation:**
- `COMMANDS_SERVERLESS.md` - Detailed command reference
- `SERVERLESS_README.md` - Architecture guide
- `SERVERLESS_MIGRATION_SUMMARY.md` - What changed

🔍 **Check Status:**
```powershell
# LocalStack
curl http://localhost:4566/_localstack/health

# Config
cat serverless-config.json

# Logs
docker-compose logs localstack | Select-String "Lambda"
```

---

## That's It!

🎉 **Your serverless e-commerce app is running!**

- Frontend: http://localhost:3000
- Backend: Fully on AWS Lambda
- Auth: AWS Cognito
- Database: DynamoDB
- Storage: S3

**No local backend server. No uvicorn. Just pure serverless! 🚀**

---

**Happy Shopping! 🛒**
