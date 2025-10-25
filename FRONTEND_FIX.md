# Frontend Authentication Fix

## Issue
The frontend was showing "Failed to fetch" because:
1. Auth pages were hardcoded to use `http://localhost:8000` (old FastAPI backend)
2. Environment variables weren't being read

## Fixed Files
✅ `frontend/src/app/auth/login/page.tsx` - Now uses `NEXT_PUBLIC_API_URL`
✅ `frontend/src/app/auth/register/page.tsx` - Now uses `NEXT_PUBLIC_API_URL`
✅ `frontend/src/app/seller/register/page.tsx` - Now uses `NEXT_PUBLIC_API_URL`

## How to Apply the Fix

### Step 1: Stop the Frontend (if running)
Press `Ctrl+C` in the terminal where `npm run dev` is running

### Step 2: Start the Frontend Fresh
```powershell
cd frontend
npm run dev
```

### Step 3: Test Authentication
1. Open http://localhost:3000
2. Click "Sign Up" 
3. Fill in the registration form
4. You should now successfully register and login!

## Environment Configuration
The frontend is configured to use:
- **API URL**: `http://localhost:4566/restapis/mxdl0slmed/dev/_user_request_`
- **Cognito User Pool**: `us-east-1_ac57e74bc7114fe687f81286007a1758`
- **Cognito Client ID**: `ub93cjj66roy6491ztft1s625x`

These are automatically set in `frontend/.env.local`

## Verification
Test the API directly:
```powershell
python -c "import requests; r = requests.post('http://localhost:4566/restapis/mxdl0slmed/dev/_user_request_/api/auth/register', json={'email':'test@example.com','password':'Test123!','first_name':'Test','last_name':'User','user_type':'buyer'}); print(r.status_code, r.json())"
```

Should return: `200 {'message': 'User registered successfully'}`
