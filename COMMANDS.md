# 🚀 Complete Command Reference

## Initial Setup (One-time)

### 1. Install Dependencies

**Backend:**
```powershell
cd backend
pip install -r requirements.txt
```

**Frontend:**
```powershell
cd frontend
npm install
# or
pnpm install
```

---

## Starting the Application

### Option 1: Manual Start (Recommended for Development)

**Terminal 1 - LocalStack:**
```powershell
# If using Docker Compose:
docker-compose up localstack

# Or if using LocalStack CLI:
localstack start
```

**Terminal 2 - Deploy Infrastructure:**
```powershell
# Wait for LocalStack to be ready, then:
python scripts\deploy-infrastructure.py
```

**Terminal 3 - Seed Database:**
```powershell
# After infrastructure is deployed:
python scripts\seed-products-corrected.py
```

**Terminal 4 - Backend:**
```powershell
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 5 - Frontend:**
```powershell
cd frontend
npm run dev
```

---

### Option 2: Using Docker Compose (All Services)

```powershell
docker-compose up
```

This will start:
- LocalStack
- Backend (FastAPI)
- Frontend (Next.js)

---

## Access URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Main application |
| Backend API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/api/docs | Swagger UI |
| API Redoc | http://localhost:8000/api/redoc | ReDoc |
| LocalStack | http://localhost:4566 | AWS services |
| LocalStack Health | http://localhost:4566/_localstack/health | Service status |

---

## Development Commands

### Backend Commands

```powershell
# Start backend with auto-reload
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest

# Check code style
flake8

# Format code
black .
```

### Frontend Commands

```powershell
# Start development server
cd frontend
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint

# Type check
npm run type-check
```

---

## Database Commands

### Deploy Infrastructure
```powershell
# Create all DynamoDB tables, S3 buckets, etc.
python scripts\deploy-infrastructure.py
```

### Seed Database
```powershell
# Add sample products (39 products)
python scripts\seed-products-corrected.py

# Add more products (original 5)
python scripts\seed-data.py
```

### Clear All Data
```powershell
# Stop LocalStack
docker-compose down

# Remove volumes
docker-compose down -v

# Restart LocalStack
docker-compose up localstack

# Redeploy infrastructure
python scripts\deploy-infrastructure.py

# Reseed data
python scripts\seed-products-corrected.py
```

---

## AWS CLI Commands (LocalStack)

### Set Environment Variables
```powershell
$env:AWS_ACCESS_KEY_ID="test"
$env:AWS_SECRET_ACCESS_KEY="test"
$env:AWS_DEFAULT_REGION="us-east-1"
```

### DynamoDB Commands

**List Tables:**
```powershell
aws dynamodb list-tables --endpoint-url=http://localhost:4566
```

**Scan Products Table:**
```powershell
aws dynamodb scan --table-name ekart-products-dev --endpoint-url=http://localhost:4566
```

**Get Item:**
```powershell
aws dynamodb get-item `
  --table-name ekart-products-dev `
  --key '{\"product_id\":{\"S\":\"YOUR_PRODUCT_ID\"}}' `
  --endpoint-url=http://localhost:4566
```

**Delete Table:**
```powershell
aws dynamodb delete-table --table-name ekart-products-dev --endpoint-url=http://localhost:4566
```

### S3 Commands

**List Buckets:**
```powershell
aws s3 ls --endpoint-url=http://localhost:4566
```

**List Objects:**
```powershell
aws s3 ls s3://ekart-product-images-dev --endpoint-url=http://localhost:4566
```

### Cognito Commands

**List User Pools:**
```powershell
aws cognito-idp list-user-pools --max-results 10 --endpoint-url=http://localhost:4566
```

---

## Testing Commands

### Backend API Tests

**Health Check:**
```powershell
curl http://localhost:8000/health
```

**Get All Products:**
```powershell
curl http://localhost:8000/api/products/
```

**Register User:**
```powershell
curl -X POST http://localhost:8000/api/auth/register/ `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"test@example.com\",\"password\":\"test123\",\"first_name\":\"Test\",\"last_name\":\"User\",\"user_type\":\"seller\"}'
```

**Login:**
```powershell
curl -X POST http://localhost:8000/api/auth/login/ `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"test@example.com\",\"password\":\"test123\"}'
```

---

## Troubleshooting Commands

### Check Service Status

**LocalStack Health:**
```powershell
curl http://localhost:4566/_localstack/health
```

**Backend Health:**
```powershell
curl http://localhost:8000/health
```

**Frontend:**
Open http://localhost:3000 in browser

### View Logs

**Docker Compose Logs:**
```powershell
# All services
docker-compose logs

# Specific service
docker-compose logs localstack
docker-compose logs backend
docker-compose logs frontend

# Follow logs
docker-compose logs -f
```

**Backend Logs:**
Already printed to terminal when running uvicorn

**Frontend Logs:**
Already printed to terminal when running npm run dev

### Restart Services

**Restart Backend:**
```powershell
# Ctrl+C to stop, then:
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Restart Frontend:**
```powershell
# Ctrl+C to stop, then:
cd frontend
npm run dev
```

**Restart LocalStack:**
```powershell
docker-compose restart localstack
```

---

## Cleanup Commands

### Stop All Services
```powershell
# If using Docker Compose:
docker-compose down

# Stop individual services with Ctrl+C in their terminals
```

### Remove All Data
```powershell
# Stop and remove volumes
docker-compose down -v

# Remove node_modules (if needed)
cd frontend
Remove-Item -Recurse -Force node_modules

# Remove Python cache
cd backend
Remove-Item -Recurse -Force __pycache__
```

### Fresh Start
```powershell
# 1. Stop everything
docker-compose down -v

# 2. Start LocalStack
docker-compose up localstack

# 3. Wait for LocalStack to be ready (10-15 seconds)

# 4. Deploy infrastructure
python scripts\deploy-infrastructure.py

# 5. Seed database
python scripts\seed-products-corrected.py

# 6. Start backend
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 7. Start frontend (in new terminal)
cd frontend
npm run dev
```

---

## Development Workflow

### Making Changes to Backend

1. Edit Python files in `backend/`
2. Save file
3. Uvicorn auto-reloads
4. Test endpoint with curl or frontend

### Making Changes to Frontend

1. Edit TypeScript/React files in `frontend/src/`
2. Save file
3. Next.js hot-reloads
4. Browser automatically refreshes
5. Check browser console for errors

### Adding New API Endpoint

1. Create route in `backend/api/[module]/routes.py`
2. Add route to `backend/main.py`
3. Restart backend
4. Test with curl
5. Add frontend integration

### Adding New Frontend Page

1. Create page in `frontend/src/app/[path]/page.tsx`
2. Save file
3. Navigate to http://localhost:3000/[path]
4. Add link in Header/Footer if needed

---

## Production Commands

### Build for Production

**Backend:**
```powershell
# Backend is ready for production as-is
# Just set environment variables for production AWS
```

**Frontend:**
```powershell
cd frontend
npm run build
npm start
```

### Environment Variables

**Backend (.env):**
```
ENVIRONMENT=production
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_real_key
AWS_SECRET_ACCESS_KEY=your_real_secret
COGNITO_USER_POOL_ID=your_pool_id
```

**Frontend (.env.local):**
```
NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api
```

---

## Quick Reference

### Start Everything (Development)
```powershell
# Terminal 1
docker-compose up localstack

# Terminal 2 (after LocalStack is ready)
python scripts\deploy-infrastructure.py
python scripts\seed-products-corrected.py

# Terminal 3
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 4
cd frontend
npm run dev
```

### Stop Everything
```powershell
# Press Ctrl+C in each terminal
# Then:
docker-compose down
```

### Reset Database
```powershell
docker-compose restart localstack
python scripts\deploy-infrastructure.py
python scripts\seed-products-corrected.py
```

---

## Common Port Usage

| Port | Service | Can Change? |
|------|---------|-------------|
| 3000 | Frontend | Yes (package.json) |
| 8000 | Backend | Yes (uvicorn command) |
| 4566 | LocalStack | Yes (docker-compose.yml) |

---

## Git Commands (Optional)

```powershell
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit"

# Create .gitignore
echo "node_modules/
__pycache__/
.env
.env.local
*.pyc
.next/" > .gitignore
```

---

**💡 Pro Tips:**

1. Always start LocalStack first
2. Wait 10-15 seconds after LocalStack starts before deploying infrastructure
3. Deploy infrastructure before seeding data
4. Use `--reload` flag for development
5. Check browser console for frontend errors
6. Check terminal output for backend errors
7. Use curl to test API endpoints directly

---

**🎯 Most Common Commands:**

```powershell
# Start backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Start frontend
npm run dev

# Deploy infrastructure
python scripts\deploy-infrastructure.py

# Seed data
python scripts\seed-products-corrected.py
```

Save these commands for quick reference!
