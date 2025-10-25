# Quick Start Guide for EKart Store

## Prerequisites Installed ✓
- Python 3.9+ with dependencies installed
- Node.js 18+ with pnpm/npm
- LocalStack (Docker)
- AWS CLI

## Step-by-Step Setup

### 1. Start LocalStack
Open a new terminal and run:
```powershell
docker-compose up -d localstack
```

Wait for LocalStack to be ready (check with `docker logs ekart-localstack`).

### 2. Set AWS Environment Variables
```powershell
$env:AWS_ACCESS_KEY_ID="test"
$env:AWS_SECRET_ACCESS_KEY="test"
$env:AWS_DEFAULT_REGION="us-east-1"
```

### 3. Deploy Infrastructure to LocalStack
```powershell
aws --endpoint-url=http://localhost:4566 cloudformation deploy --template-file infrastructure/cloudformation/main.yml --stack-name ekart-dev --parameter-overrides Environment=dev --capabilities CAPABILITY_IAM
```

### 4. Seed Sample Data (Optional)
```powershell
python scripts/seed-data.py
```

### 5. Start Backend API
Open a new terminal:
```powershell
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. Start Frontend
Open another new terminal:
```powershell
cd frontend
npm run dev
```

## Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/api/docs
- **API Docs (ReDoc)**: http://localhost:8000/api/redoc
- **LocalStack Health**: http://localhost:4566/_localstack/health

## Verify Everything is Working

### Test Backend Health
```powershell
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"healthy","service":"ekart-api"}
```

### Test Products API
```powershell
curl http://localhost:8000/api/products/
```

### Run Integration Tests
```powershell
python scripts/test-integration.py
```

## Common Issues and Solutions

### Issue: CloudFormation deployment fails
**Solution**: Make sure LocalStack is running and AWS credentials are set:
```powershell
$env:AWS_ACCESS_KEY_ID="test"
$env:AWS_SECRET_ACCESS_KEY="test"
```

### Issue: Backend fails to start
**Solution**: Check that all dependencies are installed:
```powershell
cd backend
pip install -r requirements.txt
```

### Issue: Frontend fails to start
**Solution**: Check that all dependencies are installed:
```powershell
cd frontend
npm install
```

### Issue: Cannot connect to LocalStack
**Solution**: Check LocalStack is running:
```powershell
docker ps | findstr localstack
```

If not running:
```powershell
docker-compose up -d localstack
```

## Development Workflow

1. **Make changes to backend code** - The API will auto-reload
2. **Make changes to frontend code** - Next.js will hot-reload
3. **Test your changes** - Use the API docs at http://localhost:8000/api/docs
4. **Run tests** - `pytest` for backend, `npm test` for frontend

## Available Scripts

### Backend
- `uvicorn main:app --reload` - Start development server
- `pytest` - Run tests
- `black .` - Format code
- `flake8 .` - Lint code

### Frontend
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Lint code

## Next Steps

1. Explore the API documentation at http://localhost:8000/api/docs
2. Browse the frontend at http://localhost:3000
3. Check the architecture docs in `docs/architecture.md`
4. Review the API documentation in `docs/api-documentation.md`

## Stopping the Application

1. Press `Ctrl+C` in the backend terminal
2. Press `Ctrl+C` in the frontend terminal
3. Stop LocalStack:
```powershell
docker-compose down
```

---

**Happy coding! 🚀**
