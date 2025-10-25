# Stripe Payment Integration - Quick Setup Script

Write-Host "=== EKart Store - Stripe Payment Setup ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Install Backend Dependencies
Write-Host "Step 1: Installing backend dependencies..." -ForegroundColor Yellow
Set-Location backend
pip install stripe==8.0.0
Write-Host "✓ Backend dependencies installed" -ForegroundColor Green
Write-Host ""

# Step 2: Install Frontend Dependencies
Write-Host "Step 2: Installing frontend dependencies..." -ForegroundColor Yellow
Set-Location ..\frontend
npm install @stripe/stripe-js@^2.4.0 @stripe/react-stripe-js@^2.4.0
Write-Host "✓ Frontend dependencies installed" -ForegroundColor Green
Write-Host ""

# Step 3: Verify LocalStack Stripe Extension
Write-Host "Step 3: Verifying LocalStack Stripe extension..." -ForegroundColor Yellow
docker exec -it localstack-main localstack extensions list
Write-Host ""

Write-Host "=== Setup Complete! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Restart backend: cd backend; uvicorn main:app --reload --host 0.0.0.0 --port 8000"
Write-Host "2. Restart frontend: cd frontend; npm run dev"
Write-Host "3. Login and add items to cart"
Write-Host "4. Click 'Proceed to Checkout' in cart page"
Write-Host "5. Use test card: 4242 4242 4242 4242"
Write-Host ""
Write-Host "See STRIPE_SETUP.md for detailed documentation" -ForegroundColor Yellow
