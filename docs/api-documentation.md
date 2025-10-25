# EKart Store API Documentation

## Base URL
- Local: `http://localhost:8000/api`
- Production: `https://api.ekart.com/api`

## Authentication
All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <token>
```

## Endpoints

### Products

#### GET /products
Get all products with optional filters
- Query params: category, min_price, max_price, brand, seller_id, page, per_page
- Response: Array of products

#### GET /products/{id}
Get a specific product by ID
- Response: Product object

#### POST /products
Create a new product (sellers only)
- Request body: ProductCreate
- Response: Created product

#### PUT /products/{id}
Update a product (owner only)
- Request body: ProductUpdate
- Response: Updated product

#### DELETE /products/{id}
Delete a product (owner only)
- Response: Success message

### Orders

#### GET /orders
Get user's orders
- Response: Array of orders

#### POST /orders
Create a new order
- Request body: OrderCreate
- Response: Created order

### Cart

#### GET /cart
Get user's shopping cart
- Response: Cart object with items

#### POST /cart/items
Add item to cart
- Request body: CartItem
- Response: Updated cart

### Authentication

#### POST /auth/register
Register a new user
- Request body: UserCreate
- Response: User profile + token

#### POST /auth/login
Login with email and password
- Request body: UserLogin
- Response: User profile + token

## Error Responses

All endpoints return standard HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error
