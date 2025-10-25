# 🔐 Test Credentials

## How to Test the Application

### Step 1: Start Services
Make sure all services are running:
1. LocalStack
2. Backend (port 8000)
3. Frontend (port 3000)

### Step 2: Register a Seller Account

**URL:** http://localhost:3000/seller/register

**Test Data:**
```
First Name: John
Last Name: Seller
Email: john.seller@test.com
Phone: +1-555-0100
Password: seller123
Confirm Password: seller123
```

After registration, you'll be automatically logged in and redirected to the seller dashboard.

---

### Step 3: Or Login with Existing Account

**URL:** http://localhost:3000/auth/login

**Credentials:**
```
Email: john.seller@test.com
Password: seller123
```

---

### Step 4: Add a Product

Once logged in as a seller:

1. Go to http://localhost:3000/seller/dashboard
2. Click "Add New Product" button
3. Fill in the form:

**Sample Product Data:**
```
Title: Premium Wireless Headphones
Description: High-quality noise-cancelling headphones with 30-hour battery life
Category: Electronics
Price: 199.99
Stock Quantity: 50
Brand: TechBrand
Tags: audio, headphones, wireless, noise-cancelling
Currency: USD
```

4. Click "Create Product"
5. You'll be redirected back to the dashboard
6. Your new product should appear in the products table

---

### Step 5: Test Customer Account

**URL:** http://localhost:3000/auth/register

**Test Data:**
```
First Name: Jane
Last Name: Customer
Email: jane.customer@test.com
Phone: +1-555-0200
Password: customer123
Confirm Password: customer123
User Type: customer (default)
```

**Login with:**
```
Email: jane.customer@test.com
Password: customer123
```

Customers will be redirected to the homepage after login.

---

## Quick Test Scenarios

### Scenario 1: Complete Seller Workflow
1. ✅ Register as seller
2. ✅ View empty dashboard
3. ✅ Add first product
4. ✅ View product in dashboard table
5. ✅ Add second product
6. ✅ See stats update

### Scenario 2: Login & Logout
1. ✅ Register account
2. ✅ Logout (clear localStorage)
3. ✅ Login with credentials
4. ✅ Access dashboard
5. ✅ Verify user_type routing

### Scenario 3: Product Management
1. ✅ Login as seller
2. ✅ Add product with all fields
3. ✅ Verify price displays correctly ($199.99)
4. ✅ Verify stock displays correctly (50)
5. ✅ Verify status is Active

---

## API Testing with curl

### Test Registration
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123",
    "first_name": "Test",
    "last_name": "User",
    "user_type": "seller"
  }'
```

### Test Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123"
  }'
```

### Test Create Product (requires token)
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "Test Product",
    "description": "Test Description",
    "category": "Electronics",
    "price": 99.99,
    "stock_quantity": 10,
    "brand": "TestBrand",
    "tags": ["test"],
    "currency": "USD"
  }'
```

### Test Get Products
```bash
curl http://localhost:8000/api/products/
```

---

## Browser Testing

### Check localStorage After Login
Open browser console (F12) and run:
```javascript
console.log({
  access_token: localStorage.getItem('access_token'),
  user_id: localStorage.getItem('user_id'),
  user_email: localStorage.getItem('user_email'),
  user_type: localStorage.getItem('user_type')
});
```

### Manual Logout
```javascript
localStorage.clear();
window.location.href = '/';
```

---

## Database Verification

### Check Users Table
```python
import boto3

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

users_table = dynamodb.Table('ekart-users-dev')
response = users_table.scan()
print(response['Items'])
```

### Check Products Table
```python
products_table = dynamodb.Table('ekart-products-dev')
response = products_table.scan()
print(f"Total products: {len(response['Items'])}")
for product in response['Items']:
    print(f"- {product['title']}: ${product['price']}")
```

---

## Common Issues & Solutions

### Issue: "Invalid email or password"
- Check email is correct
- Password is case-sensitive
- Make sure user is registered first

### Issue: "Only verified sellers can create products"
- Make sure you registered as a seller (user_type: "seller")
- Check localStorage has user_type === "seller"

### Issue: "Product price not showing"
- Backend returns price as float
- Frontend checks type before calling .toFixed()
- Should display "$XX.XX" format

### Issue: "Redirected to login after registration"
- Check localStorage has access_token
- Check token format is "user_id:hash"
- Verify backend returned all fields

---

## Troubleshooting Commands

### Restart Backend
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Restart Frontend
```bash
cd frontend
npm run dev
```

### Clear Database and Reseed
```bash
python scripts/deploy-infrastructure.py
python scripts/seed-products-corrected.py
```

---

## Expected Behavior

### ✅ Registration Success
- Form clears
- Redirect to appropriate page
- localStorage populated
- No error messages

### ✅ Login Success
- Redirect based on user_type
- Seller → /seller/dashboard
- Customer → /
- Dashboard loads without errors

### ✅ Dashboard Display
- Stats cards show numbers
- Product table displays correctly
- Prices formatted as $XX.XX
- Stock shows as integer
- Active/Inactive badges colored correctly

### ✅ Add Product Success
- Form validates all fields
- API call succeeds
- Redirect to dashboard
- New product appears in table

---

**Happy Testing! 🚀**
